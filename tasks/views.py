# ✅ views.py (Completely Modified with Fixes for Due Date and Assignee)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils.dateparse import parse_date
from django.utils import timezone
from django.http import JsonResponse

from .models import Task
from .forms import TaskForm
from .decorators import is_project_manager_or_admin
from project.decorators import is_project_manager_or_admin
from project.ai_utils import get_best_user_for_task
from tasks.utils import get_evenly_distributed_due_date  # ✅ NEW

import logging
logger = logging.getLogger(__name__)

@login_required
def task_list(request):
    query = request.GET.get('q')
    status_filter = request.GET.get('status')
    tasks = Task.objects.all()

    if query:
        tasks = tasks.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(project__title__icontains=query) |
            Q(assignee__username__icontains=query)
        ).distinct()

    if status_filter and status_filter != 'all':
        tasks = tasks.filter(status=status_filter)

    context = {
        'tasks': tasks,
        'query': query,
        'status_filter': status_filter or 'all',
    }
    return render(request, 'tasks/task_tab.html', context)


@login_required
@is_project_manager_or_admin
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            project = task.project

            # ✅ AI Assignee
            if not task.assignee:
                try:
                    best_user = get_best_user_for_task(task.title)
                    if best_user:
                        task.assignee = best_user
                        logger.info(f"✅ Assigned to {best_user.username}")
                except Exception as e:
                    logger.error(f"❌ AI Error: {e}")

            # ✅ Correctly calculate due date between project.start_date and end_date
            if not task.due_date:
                total_tasks = Task.objects.filter(project=project).count()
                task_index = total_tasks  # current task will be the next
                task.due_date = get_evenly_distributed_due_date(project, task_index, total_tasks + 1)

            task.save()
            form.save_m2m()
            messages.success(request, f"Task created! Assigned to {task.assignee.username if task.assignee else 'No one'}")
            return redirect('tasks:tasks_tab')
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = TaskForm()

    return render(request, 'tasks/task_create.html', {'form': form})

@login_required
@is_project_manager_or_admin
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully!")
            return redirect('tasks:tasks_tab')
        else:
            messages.error(request, "Form validation failed. Please correct the errors.")
    else:
        form = TaskForm(instance=task)

    return render(request, 'tasks/task_edit.html', {'form': form, 'task': task})


@login_required
def tasks_tab(request):
    query = request.GET.get('q')
    status_filter = request.GET.get('status')

    user = request.user

    # Initial queryset with prefetching
    tasks = Task.objects.select_related('assignee', 'project').all()

    # --- Filter based on user role ---
    if user.role == 'admin':
        # Admin sees all tasks
        tasks = tasks
    elif user.role == 'manager':
        # Project Manager sees tasks only for their projects
        tasks = tasks.filter(project__created_by=user)
    else:
        # Normal user sees only assigned tasks
        tasks = tasks.filter(assignee=user)

    # --- Auto update status ---
    for task in tasks:
        task.auto_update_status()

    # --- Search filter ---
    if query:
        tasks = tasks.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(project__title__icontains=query) |
            Q(assignee__username__icontains=query)
        ).distinct()

    # --- Status filter ---
    if status_filter and status_filter != 'all':
        tasks = tasks.filter(status=status_filter)

    context = {
        'tasks': tasks,
        'query': query,
        'status_filter': status_filter or 'all',
    }
    return render(request, 'tasks/tasks_tab.html', context)




@login_required
@is_project_manager_or_admin
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    messages.success(request, "Task deleted successfully!")
    return redirect('tasks:tasks_tab')


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/task_detail.html', {'task': task})


@login_required
def mark_task_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.progress = 100
    task.status = 'completed'
    task.save()
    return redirect('tasks:task_detail', pk=task_id)


@login_required
def tasks_by_date(request):
    date_str = request.GET.get('date')
    if not date_str:
        return JsonResponse({'error': 'Date parameter is required'}, status=400)

    try:
        date = parse_date(date_str)
        tasks = Task.objects.filter(due_date=date)
        task_data = [
            {
                'title': task.title,
                'description': task.description,
                'status': task.status,
                'project': task.project.title if task.project else "No Project",
            }
            for task in tasks
        ]
        return JsonResponse({'tasks': task_data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
