from django.utils import timezone
from .models import Task

def check_and_notify_past_due_tasks(user):
    # Actuall date
    current_date = timezone.now().date()

    overdue_tasks = Task.objects.filter(due_date__lt=current_date, completed=False)
    message = f"You have  tasks overdue in the past days."

    return len(overdue_tasks) == 0
