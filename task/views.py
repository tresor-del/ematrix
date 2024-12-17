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
from django.contrib import messages
from django.db.models import Q

from .forms import TaskForm, ProjectForm, GroupTaskForm
from .models import CustomUser, Task, Notification, Friends, Project, Comment, GroupTask



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
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == 'POST':
        task.delete() 
        
        return JsonResponse({'success': True}, status=200)
    
    task.delete()
    messages.warning(request, f'Task "{task.title}" deleted!')
    
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
    projects = Project.objects.filter( Q(owner=request.user)|Q(members=request.user))

    user_tasks = GroupTask.objects.filter(project__in=projects, assigned_to=request.user)
    projects_tasks_completed = user_tasks.filter(status='Completed')
    pending_project_tasks = user_tasks.filter(status='Pending')

    notifications = Notification.objects.filter(user=request.user, is_read=False).all()
    context = {
        'tasks': tasks,
        'projects': len(projects),
        'projects_tasks_completed': len(projects_tasks_completed),
        'pending_project_tasks': len(pending_project_tasks),
        'task_count': task_count,
        'completed_task_count': completed_task_count,
        'pending_task_count': pending_task_count,
        'notifications': notifications
    }

    return render(request, 'task/dashboard.html', context)

# Notifications views

@csrf_exempt
def notifications(request):
    all_notifications = Notification.objects.filter(user=request.user)

    if all_notifications.exists():
        all_notifications.update(is_read=True)
        return render(request, 'task/notifications.html',{
            'all_notifications': all_notifications,
            'notifications': notifications
        })

    else:
        print("Aucune notification à mettre à jour.")
        return render(request, 'task/notifications.html',{
            'notifications': notifications,
            'all_notifications': all_notifications
        })

@csrf_exempt
def delete_notification(request, notification_id):
    # Fetch the task object using the task_id or return 404 if not found
    notification = get_object_or_404(Notification, id=notification_id)
    
    # Ensure that the request method is POST (delete operation)
    if request.method == 'POST':
        notification.delete()  # Delete the task from the database
        
        # Return a JSON response to indicate success
        return JsonResponse({'success': True}, status=200)

@csrf_exempt
def delete_all_notification(request):
    notifications = Notification.objects.filter(user=request.user)
    for notification in notifications:
        notification.delete()
    return JsonResponse({'success':True}, status=200)

#Calendar views

def calendar(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False).all()
    return render(request, 'task/calendar.html', {
        'notifications': notifications
    })

def calendar_tasks(request, due_date):
        tasks = Task.objects.filter(author=request.user, due_date=due_date).all()
        return render(request, "task/calendar_tasks.html", {"tasks": tasks, "formatted_date": due_date})

#Profile views

def profile_view(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    visitor = request.user
    notifications = Notification.objects.filter(user=request.user, is_read=False).all()
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
    return render(request, 'task/profile.html', {
        'user': user,
        'visitor': visitor,
        'task_count': task_count,
        'notifications': notifications,
        'completed_task_count': completed_task_count,
        'pending_task_count': pending_task_count
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
    try:
        user = request.user

        friends_instance = Friends.objects.filter(user=user).first()

        if friends_instance:
            friends = friends_instance.get_friends()  
        else:
            friends = []  

        return render(request, 'collaborators/index.html', {
            'notifications': notifications,
            'friends': friends
        })
    except Exception as e:
        print(e)
        return render(request, 'collaborators/index.html', {
            'notifications': notifications,
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
    Notification.objects.create(user=user, sender=request.user, message=message)
    return JsonResponse({'message': 'notification sent successfully!'}, status=200)
    
def confirm_invitation(request, user_id):
    friends, created = Friends.objects.get_or_create(user=request.user)
    friend = get_object_or_404(CustomUser, pk=user_id)
    u_friends, created = Friends.objects.get_or_create(user=friend)
    friends.friends.add(friend)
    u_friends.friends.add(request.user)
    Notification.objects.create(user=friend, message=f'${request.user} is your friend now')
    return JsonResponse({'success': True}, status=200)

# Project

def project(request):
    user = request.user
    user_id = user.id
    notifications = Notification.objects.filter(user=user_id, is_read=False).all()
    projects = Project.objects.filter(
        Q(members=user_id) | Q(owner=user_id)
    )    
    return render(request, 'project/index.html', {
        'notifications': notifications,
        'projects': projects
    })


def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, owner=request.user )
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            project.members.add(request.user)
            form.save_m2m()  
            print("a")
            for member in request.POST['members']:
                user = get_object_or_404(CustomUser, pk=member)
                Notification.objects.create(user=user, message=f'{request.user} created {request.POST['name']} and added you')
            return redirect('task:project')
        else:
            return redirect('task:project')
    else:
        user = request.user
        user_id = user.id
        form = ProjectForm(owner=user_id)
        return render(request, 'project/create_project.html', {'form': form})
    
def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    try:
        comments = get_list_or_404(Comment, project=project)
    except:
        comments = None
    return render(request, 'project/project_detail.html', {
        'project':project,
        'notifications': notifications,
        'comments': comments
    })

def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    for member in project.members.all():
        Notification.objects.create(user=member, message=f'{request.user} deleted the {project.name} project')
    project.delete()
    messages.warning(request, f'Project  deleted !')
    return redirect('task:project')

def edit_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user  
            project.save()
            messages.success(request, f'Project {project.name} updated successfully!')
            return redirect('task:project')
        else:
            form = ProjectForm(instance=project)
            return render(request,'project/edit_project.html', {
            'form': form,
            'project': project 
        })
    else:
        form = ProjectForm(instance=project) 
        return render(request, 'project/edit_project.html', {
            'form': form,
            'project': project 
        })
    
def search_members(request):
    query = request.GET.get('search', '').strip()
    if query:
        users = Friends.objects.filter(user=request.user, friends__username__icontains=query).values('friends__id', 'friends__username')
        print(users)
        return JsonResponse({'users': list(users)}, status=200)
    return JsonResponse({'users': []}, status=200)
    
@csrf_exempt
def add_member(request, project_id):
    if request.method == "POST" :
        project = get_object_or_404(Project, id=project_id, owner=request.user)
        data = json.loads(request.body)
        if data:
            user_id = data['userId']
        try:
            user = CustomUser.objects.get(pk= int(user_id) )
            if user not in project.members.all():
                project.members.add(user)
                Notification.objects.create(user=user, sender=request.user, message=f"{request.user}, added you to '{project.name}' project")
                return JsonResponse({"message": f" has been added to the project."}, status=200)
            else:
                return JsonResponse({"error": f"is already a member of the project."}, status=400)
        except CustomUser.DoesNotExist:
            return JsonResponse({"error": f"User  does not exist."}, status=404)

    return JsonResponse({"error": "Invalid request."}, status=400)

@csrf_exempt
def remove_member(request, project_id):
    if request.method == "POST":
        project = get_object_or_404(Project, id=project_id, owner=request.user)
        data = json.loads(request.body)
        if data:
            user_id = data['userId']
        try:
            user = CustomUser.objects.get(pk=int(user_id))
            if user in project.members.all():
                project.members.remove(user)
                Notification.objects.create(user=user, sender=request.user, message=f"{request.user}, deleted you from '{project.name}' project")
                return JsonResponse({"message": f" has been removed from the project."}, status=200)
            else:
                return JsonResponse({"error": f"is not a member of the project."}, status=400)
        except CustomUser.DoesNotExist:
            return JsonResponse({"error": f"User  does not exist."}, status=404)

    return JsonResponse({"error": "Invalid request."}, status=400)


def create_project_task(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        form = GroupTaskForm(request.POST, owner=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect ('task:project_detail', project_id=project_id)
        print(form.errors)
        return redirect('task:project_detail', project_id=project_id)
    form = GroupTaskForm(owner=request.user)
    return render(request, 'project/new_task.html', {
        'form': form,
        'project': project
    })

def comment(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        comment = request.POST.get('comment')
        if comment:
            Comment.objects.create(author=request.user, project=project, comment=comment)
            return redirect ('task:project_detail', project_id=project_id)
        print(comment.errors)
        return redirect('task:project_detail', project_id=project_id)
    
def get_out_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    project.members.remove(request.user)
    return redirect('task:project')

@csrf_exempt
def change_status(request,project_id, task_id):
    project = get_object_or_404(Project, pk=project_id)
    task = get_object_or_404(GroupTask, pk=task_id)
    if request.method in ['PUT', 'POST']:
        try:
            data = json.loads(request.body)
            if 'status' in data:
                task.status = data['status']
                task.save()  # Persist the change to the database
                return JsonResponse({'message': 'Status changed successfully'}, status=200)
            else:
                return JsonResponse({'error': 'Missing "status" field in request data'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed. Use PUT or POST.'}, status=405)

def project_task_detail(request, task_id):
    task = get_object_or_404(GroupTask, pk=task_id)
    return render(request, 'project/task_detail.html',{
        'task': task
    })