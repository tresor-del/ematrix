from django.utils import timezone
from .models import Task, Notification

def send_notificatiion(user, message):
    Notification.objects.create(user=user, message=message)


def calculate_time_remaining(due_date):
    now = timezone.now().date()
    remaining_time = due_date - now
    return remaining_time.days



def check_and_notify_past_due_tasks(user):
    # Actuall date
    current_date = timezone.now().date()

    overdue_tasks = Task.objects.filter(due_date__lt=current_date, completed=False)
    message = f"You have  tasks overdue in the past days."
    Notification.objects.create(user=user, message=message)

    return len(overdue_tasks) == 0

def clean_date(date_str):
    # Retirer les caractères indésirables
    date_str = date_str.replace("'", "").strip()
    return date_str
