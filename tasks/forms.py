from django import forms
from .models import Task
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone

User = get_user_model()

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'project',
            'start_date',
            'due_date',
            'priority',
            'assignee',       # ✅ correct
            'team_members',   # ✅ correct
            'progress',
            'commands',
            'status',
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'commands': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assignee'].queryset = User.objects.all()
        self.fields['team_members'].queryset = User.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        project = cleaned_data.get('project')
        due_date = cleaned_data.get('due_date')
        task_start_date = cleaned_data.get('start_date')

        if due_date and task_start_date and due_date.date() < task_start_date:
            raise ValidationError({'due_date': 'Task due date cannot be before the task start date.'})

        if project and due_date:
            project_start = project.start_date
            project_end = project.end_date or project.due_date

            # Normalize to aware datetimes for comparison
            start_dt = None
            end_dt = None
            if project_start:
                start_dt = timezone.make_aware(
                    timezone.datetime.combine(project_start, timezone.datetime.min.time())
                )
            if project_end:
                end_dt = timezone.make_aware(
                    timezone.datetime.combine(project_end, timezone.datetime.max.time())
                )

            if start_dt and due_date < start_dt:
                raise ValidationError({'due_date': 'Task due date must be within the project timeline (too early).'})
            if end_dt and due_date > end_dt:
                raise ValidationError({'due_date': 'Task due date must be within the project timeline (after project end).'})

        return cleaned_data
