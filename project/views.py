from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.utils.dateparse import parse_date, parse_datetime
from django.utils import timezone
from .models import Project
from .forms import ProjectForm, CustomUserCreationForm
from .utils import update_expired_projects, update_pending_projects
from .decorators import is_project_manager_or_admin
from tasks.models import Task
from project.ai_utils import assign_tasks, generate_subtasks
from tasks.utils import get_evenly_distributed_due_date
from notification.utils import notify_user

@login_required
def dashboard(request):
    update_expired_projects()
    update_pending_projects()
    if request.user.role == 'admin':
        projects = Project.objects.all()
    elif request.user.role == 'manager':
        projects = Project.objects.filter(created_by=request.user)
    else:
        projects = Project.objects.filter(assigned_users=request.user)
    return render(request, 'data/dashboard.html', {'projects': projects})

@login_required
def project_list(request):
    update_expired_projects()
    update_pending_projects()
    status_filter = request.GET.get('status')
    if status_filter in ['pending', 'current', 'completed', 'failed']:
        projects = Project.objects.filter(status=status_filter)
    else:
        projects = Project.objects.all()
    return render(request, 'project/project_tab.html', {'projects': projects})

@login_required
def project_detail(request, pk):
    update_expired_projects()
    update_pending_projects()
    project = get_object_or_404(Project, pk=pk)

    if request.user.role == 'admin' or \
       (request.user.role == 'manager' and project.created_by == request.user) or \
       request.user in project.assigned_users.all():
        return render(request, 'project/project_detail.html', {'project': project})
    else:
        messages.error(request, "You do not have permission to view this project.")
        return redirect('project:project_tab')

@login_required
@is_project_manager_or_admin
def project_create(request):
    update_expired_projects()
    update_pending_projects()

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            if Project.objects.filter(title__iexact=title).exists():
                messages.error(request, f"⚠️ A project with the title '{title}' already exists.")
                return render(request, 'project/project_form.html', {'form': form})

            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            form.save_m2m()

            for user in project.assigned_users.all():
                notify_user(user, f"You have been added to the project: <strong>{project.title}</strong>.", "project_created", "/project/project_tab/")

            messages.success(request, '✅ Project created successfully!')

            try:
                def to_aware_datetime_from_str(date_str):
                    if not date_str:
                        return None
                    dt = parse_datetime(str(date_str))
                    if dt is None:
                        # Fallback: try parsing as date and set to start of day
                        d = parse_date(str(date_str))
                        if d is None:
                            return None
                        # Set to end of day for safety
                        dt = timezone.datetime.combine(d, timezone.datetime.max.time())
                    if timezone.is_naive(dt):
                        dt = timezone.make_aware(dt)
                    return dt

                def clamp_due_datetime(project_obj, candidate_dt):
                    if candidate_dt is None:
                        return None
                    # Build window using project dates
                    project_start = project_obj.start_date
                    project_end = project_obj.end_date or project_obj.due_date
                    # Convert to datetimes at boundaries
                    if project_start:
                        start_dt = timezone.make_aware(
                            timezone.datetime.combine(project_start, timezone.datetime.min.time())
                        )
                        if candidate_dt < start_dt:
                            candidate_dt = start_dt
                    if project_end:
                        end_dt = timezone.make_aware(
                            timezone.datetime.combine(project_end, timezone.datetime.max.time())
                        )
                        if candidate_dt > end_dt:
                            candidate_dt = end_dt
                    return candidate_dt

                team_size = project.assigned_users.count() or 3
                team_expertise = {
                    user.username: getattr(getattr(user, 'profile', None), 'expertise', 'general')
                    for user in project.assigned_users.all()
                }

                # Generate subtasks and assignment plan
                subtasks = generate_subtasks(project.description, team_size, project.title, project.due_date)
                # Ensure AI assignments only from this project's team and use titles as keys
                assignments = assign_tasks(project.description, project.title, project.due_date, team_size, team_expertise, subtasks=subtasks)

                # Fallback totals for even distribution when needed
                total_subtasks = len(subtasks)

                for idx, subtask in enumerate(subtasks):
                    raw_due = subtask.get("due_date")
                    due_dt = to_aware_datetime_from_str(raw_due)
                    if due_dt is None:
                        due_dt = get_evenly_distributed_due_date(project, idx, total_subtasks)
                    due_dt = clamp_due_datetime(project, due_dt) if due_dt else None

                    task = Task.objects.create(
                        title=subtask["title"],
                        description=subtask.get("description", ""),
                        project=project,
                        due_date=due_dt,
                        status=subtask.get("status", "not_started"),
                        priority=subtask.get("priority", "low"),
                        progress=subtask.get("progress", 0)
                    )

                    # Helper: fallback best user from this project's team only
                    def best_user_from_team_for(title_text: str):
                        lowered = (title_text or "").lower()
                        # Prefer profile expertise match within project team
                        for member in project.assigned_users.select_related('profile').all():
                            expertise_value = getattr(getattr(member, 'profile', None), 'expertise', '') or getattr(member, 'expertise', '')
                            expertise_lower = str(expertise_value).lower()
                            if expertise_lower and (expertise_lower in lowered or any(word in lowered for word in expertise_lower.split())):
                                return member
                        # Fallback: first team member
                        return project.assigned_users.first()

                    # Apply AI assignments: prefer title as key, fallback to description
                    assignment_info = None
                    if isinstance(assignments, dict):
                        assignment_info = assignments.get(subtask.get("title")) or assignments.get(subtask.get("description"))

                    assignee_username = None
                    team_members_csv = None
                    if isinstance(assignment_info, dict):
                        assignee_username = assignment_info.get("assignee")
                        team_members_csv = assignment_info.get("team_members")
                    elif isinstance(assignment_info, str):
                        # Backward-compat: a CSV of usernames
                        team_members_csv = assignment_info

                    if assignee_username:
                        assignee_user = project.assigned_users.filter(username=assignee_username).first()
                        if assignee_user:
                            task.assignee = assignee_user
                            task.save(update_fields=["assignee"]) 
                            notify_user(assignee_user, f"You have been assigned a new task: <strong>{task.title}</strong> in project <strong>{project.title}</strong>.", "task_assigned", "/tasks/tab/")

                    # Robust fallback if AI didn't assign or the username isn't in project team
                    if not task.assignee:
                        fallback_user = best_user_from_team_for(subtask.get("title") or subtask.get("description"))
                        if fallback_user:
                            task.assignee = fallback_user
                            task.save(update_fields=["assignee"]) 

                    if team_members_csv:
                        usernames = [name.strip() for name in str(team_members_csv).split(",") if name.strip()]
                    for username in usernames:
                            member = project.assigned_users.filter(username=username).first()
                            if member:
                                task.team_members.add(member)
                                if not assignee_username or member.username != assignee_username:
                                    notify_user(member, f"You have been added as a team member to task: <strong>{task.title}</strong> in project <strong>{project.title}</strong>.", "task_assigned", "/tasks/tab/")

                messages.success(request, '✅ AI subtasks generated and assigned!')
            except Exception as e:
                messages.error(request, f'AI task generation failed: {str(e)}')

            return redirect('project:project_tab')
    else:
        form = ProjectForm()

    return render(request, 'project/project_form.html', {'form': form})

@login_required
@is_project_manager_or_admin
def project_edit(request, pk):
    update_expired_projects()
    update_pending_projects()
    project = get_object_or_404(Project, pk=pk)
    form = ProjectForm(request.POST or None, instance=project)

    if form.is_valid():
        form.save()
        messages.success(request, '✅ Project updated successfully.')
        return redirect('project_detail', pk=pk)

    return render(request, 'project/project_form.html', {'form': form})

@login_required
@is_project_manager_or_admin
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        messages.success(request, '🗑️ Project deleted successfully.')
        return redirect('project:project_tab')
    return render(request, 'project/project_confirm_delete.html', {'project': project})

@login_required
def project_tab(request):
    update_expired_projects()
    update_pending_projects()
    status_filter = request.GET.get('status')
    search_query = request.GET.get("search", "").strip()

    if request.user.role == 'admin':
        projects = Project.objects.all()
    elif request.user.role == 'manager':
        projects = Project.objects.filter(created_by=request.user)
    else:
        projects = Project.objects.filter(assigned_users=request.user)

    if status_filter:
        projects = projects.filter(status=status_filter)
    if search_query:
        projects = projects.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))

    return render(request, 'project/project_tab.html', {'projects': projects})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'project/register.html', {'form': form})

@login_required
@is_project_manager_or_admin
def generate_subtasks_api(request):
    if request.method == "POST":
        project_description = request.POST.get("description")
        team_size = int(request.POST.get("team_size", 3))
        project_title = request.POST.get("title", "Untitled Project")
        project_due_date = request.POST.get("due_date")

        if not project_due_date:
            return JsonResponse({"error": "Missing required field: due_date"}, status=400)

        try:
            subtasks = generate_subtasks(project_description, team_size, project_title, project_due_date)
            return JsonResponse({"subtasks": subtasks})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Only POST method allowed"}, status=405)

def projects_by_date(request):
    date_str = request.GET.get('date')
    if not date_str:
        return JsonResponse({'error': 'Date parameter is required'}, status=400)

    try:
        date = parse_date(date_str)
        projects = Project.objects.filter(due_date=date)
        project_data = [
            {
                'title': project.title,
                'description': project.description,
                'status': project.status,
            }
            for project in projects
        ]
        return JsonResponse({'projects': project_data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)