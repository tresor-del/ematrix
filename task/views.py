import json
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_list_or_404, redirect, render, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from collections import defaultdict
from datetime import date,datetime
from django.db.models import ExpressionWrapper, F,  IntegerField
from .utils import  send_notificatiion, check_and_notify_past_due_tasks, clean_date
from django.contrib import messages
from django.db.models import Q

from .forms import TaskForm
from .models import CustomUser, Task, Notification



## Task view

def index(request):
    if request.user.is_authenticated:
        return redirect('task:dashboard')
    return render(request, 'task/index.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('task:dashboard'))
        else:
            return render(request, 'task/login.html', {
                'message': 'Wrong Username and/or Passwort.'
            })
    return render(request, 'task/login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmation = request.POST.get('confirmation')
        profile_image = request.FILES.get('profile_image')  

        if password != confirmation:
            return render(request, 'task/register.html', {
                'message': "Passwords do not match!"
            })
        
        try:
            user = CustomUser.objects.create_user(username=username, email=email, password=password)
            if profile_image:
                user.profile_image = profile_image
                user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('task:dashboard'))
        except Exception as e:
            return render(request, 'task/register.html', {
                'message': str(e)
            })
    
    return render(request, 'task/register.html')



def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('task:index'))

#Tasks views

def tasks_view(request):
    # take all user's tasks and calculate remaining days
    tasks = Task.objects.filter(author=request.user).annotate(
        days_until_due=ExpressionWrapper(
            F('due_date') - datetime.now().date(),
            output_field=IntegerField() 
        )
    ).filter(days_until_due__gte=0).order_by('due_date')

    today = datetime.today().date()
    print(today)

    today_tasks = Task.objects.filter(author=request.user, due_date=today )
    today_tasks_count = today_tasks.count()
    today_completed_task_count = today_tasks.filter(completed=True).count()
    today_pending_task_count = today_tasks_count - today_completed_task_count 

    # grouped tasks by due date
    grouped_tasks = defaultdict(list)
    for task in tasks:
        grouped_tasks[task.due_date].append(task)

    # convert defaultdict in sorted dictionnary
    grouped_tasks = dict(sorted(grouped_tasks.items()))

    # Aapply pagination
    grouped_items = list(grouped_tasks.items())  
    paginator = Paginator(grouped_items, 1)  # 1 group per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    important_urgent_tasks = tasks.filter(priority='important and urgent')
    important_not_urgent_tasks = tasks.filter(priority='important but not urgent')
    not_important_urgent_tasks = tasks.filter(priority='not important but ugent')
    not_important_not_urgent_tasks = tasks.filter(priority='not important and not urgent')

    notifications = Notification.objects.filter(user=request.user, is_read=False).all()
    return render(request, 'task/tasks.html', {
        'grouped_tasks': grouped_tasks,
        'today': today,
        'page_obj': page_obj,
        'notifications': notifications,
        'today_completed_task_count' : today_completed_task_count,
        'today_pending_task_count' : today_pending_task_count,
        'important_urgent_tasks': important_urgent_tasks,
        'important_not_urgent_tasks': important_not_urgent_tasks,
        'not_important_urgent_tasks': not_important_urgent_tasks,
        'not_important_not_urgent_tasks':not_important_not_urgent_tasks
    })

@csrf_exempt
def delete_task(request, task_id):
    # Fetch the task object using the task_id or return 404 if not found
    task = get_object_or_404(Task, id=task_id)
    
    # Ensure that the request method is POST (delete operation)
    if request.method == 'POST':
        task.delete()  # Delete the task from the database
        
        # Return a JSON response to indicate success
        return JsonResponse({'success': True}, status=200)
    
    # Optionally show a message if it’s not a POST request (e.g., via GET or other methods)
    task.delete()
    messages.warning(request, f'Task "{task.title}" deleted!')
    
    # Redirect to the task list page (you may adjust the reverse route as needed)
    return HttpResponseRedirect(reverse('task:tasks'))



def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    days = task.remaining_days()
    return render(request, 'task/task_detail.html', {
        'task': task,
        'days': days
    })

@csrf_exempt
def task(request, task_id):
    try:
        task = get_object_or_404(Task, author=request.user, pk=task_id)
    except task.DoesNotExist:
        return JsonResponse({'error':'Task not found'}, status=400)
    
    if request.method == 'PUT':
        data = json.loads(request.body)
        if data.get('completed') is not None:
            print(data['completed'])
            task.completed = data['completed']
            task.save()
            messages.success(request, f'Task {task.title} marked as read!')
            return redirect('task:tasks')
    
    else:
        task = get_object_or_404(Task, author=request.user, pk=task_id)
        task.completed = True
        task.save()
        messages.success(request, f'Task "{task.title}" marked as completed successfully!')
        return redirect('task:tasks')
    
@csrf_exempt
def update_task(request, task_id):
    task_to_update = get_object_or_404(Task, author=request.user, pk=task_id)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task_to_update)
        
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user  
            task.save() 
            messages.success(request, f'Task "{task_to_update.title}" updated successfully!')
            return redirect('task:tasks')
        else:
            form = TaskForm(instance=task_to_update)
            return render(request, 'task/update_task.html', {
            'form': form,
            'task': task_to_update  
        })
    else:
        form = TaskForm(instance=task_to_update) 
        return render(request, 'task/update_task.html', {
            'form': form,
            'task': task_to_update  
        })


@csrf_exempt 
def new_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.save()
            messages.success(request, f'Task "{task.title}" creatted successfully!')
            return redirect('task:tasks')
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    form= TaskForm()
    return render(request, ('task/new_task.html'),{
        'form':form
    })

#Dashboard views

def dashboard(request):
    # take all tasks and calculate remaining days
    tasks = Task.objects.filter(author=request.user).annotate(
        days_until_due=ExpressionWrapper(
            F('due_date') - datetime.now().date(),
            output_field=IntegerField()  
        )
    ).filter(days_until_due__gte=0).order_by('due_date')
    
    # count pending, completed and all tasks
    task_count = tasks.count()
    completed_task_count = tasks.filter(completed=True).count()
    pending_task_count = task_count - completed_task_count
    
    notifications = Notification.objects.filter(user=request.user, is_read=False).all()
    context = {
        'tasks': tasks,
        'task_count': task_count,
        'completed_task_count': completed_task_count,
        'pending_task_count': pending_task_count,
        'notifications': notifications
    }

    return render(request, 'task/dashboard.html', context)

# Notifications views

@csrf_exempt
def notifications(request):
    if request.method == 'PUT':
        data= json.loads(request.body)
        if data :
            id = data['id']
            is_read = data['is_read']
            notification = get_object_or_404(Notification, pk=id)
            notification.is_read = is_read
    notifications = Notification.objects.filter(user=request.user).all()
    return render(request, 'task/notifications.html',{
        'notifications': notifications
    })



#Calendar views

def calendar(request):
    notifications = Notification.objects.filter(user=request.user).all()
    return render(request, 'task/calendar.html', {
        'notifications': notifications
    })

def calendar_tasks(request, due_date):
        tasks = Task.objects.filter(author=request.user, due_date=due_date).all()
        return render(request, "task/calendar_tasks.html", {"tasks": tasks, "formatted_date": due_date})

#Profile views

def profile_view(request):
    user = request.user
    notifications = Notification.objects.filter(user=request.user, is_read=False).all()
    return render(request, 'task/profile.html', {
        'user': user,
        'notifications': notifications
    })
@csrf_exempt
@login_required
def edit_profile(request):
    if request.method == 'POST':
        print('3')
        try:
            image = request.FILES.get('profile_image', request.user.profile_image)
            username = request.POST.get('username')
            if not username:
                messages.warning(request, 'username error')
                return redirect('task:profile')
            email = request.POST.get('email')

            customuser = request.user
            customuser.profile_image = image
            customuser.username = username
            customuser.email = email

            customuser.save()
            messages.success(request, 'Profile Updated successfully!')
            return redirect('task:profile')
        except Exception as e:
            messages.warning(request, str(e))
            return redirect('task:profile')

    return render(request, 'task/edit_profile.html', {
        'user': request.user,
        })

# collaboration

def collaborators_views(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False).all()
    return render(request, 'collaborators/index.html', {
        'notifications': notifications
    })

def search_users(request):
    query = request.GET.get('search', '').strip()
    if query:
        users = CustomUser.objects.filter(username__icontains=query).values('id', 'username')
        return JsonResponse({'users': list(users)}, status=200)
    return JsonResponse({'users': []}, status=200)

def invite_user(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    message = f'{request.user}, invited you to be his friend'
    Notification.objects.create(user=user, message=message)
    return JsonResponse({'message': 'notification sent successfully!'}, status=200)
    

# Project

def project(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False).all()
    return render(request, 'project/index.html', {
        'notifications': notifications
    })