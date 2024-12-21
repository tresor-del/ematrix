import json
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_list_or_404, redirect, render, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse
from collections import defaultdict
from datetime import date,datetime
from django.db.models import ExpressionWrapper, F,  IntegerField
from django.contrib import messages
from django.db.models import Q

from .forms import TaskForm, ProjectForm, GroupTaskForm
from .models import CustomUser, Task, Notification, Friends, Project, Comment, GroupTask, ProjectActivity



## Task view

def index(request):
    if request.user.is_authenticated:
        return redirect('task:tasks')
    return render(request, 'task/index.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('task:tasks'))
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
            return HttpResponseRedirect(reverse('task:tasks'))
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
        'today': today,
        'tasks': tasks,
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





@csrf_exempt
def task(request, task_id):
    try:
        task = get_object_or_404(Task, author=request.user, pk=task_id)
    except task.DoesNotExist:
        return JsonResponse({'error':'Task not found'}, status=400)
    
    if request.method == 'PUT':
        data = json.loads(request.body)
        if data.get('name')== 'Completed':
            task.completed = True
            task.save()
            return JsonResponse({'message': 'Task completed'}, status=200)
        elif data.get('name')== 'Pending':
            task.completed = False
            task.save()
            return JsonResponse({'message': 'Task retored'}, status=200)
        else:
            return JsonResponse({'error': 'status is none'}, status=400)
    elif request.method == 'DELETE':
        task.delete()
        return JsonResponse({'message': 'Task completed'}, status=200)
    


@csrf_exempt 
def new_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.save()
            return JsonResponse({
                "message": "Task created successfully",
                "task": {
                    "id": task.id,
                    "title": task.title,
                    "priority": task.priority,
                    "completed": False
                }
            }, status=200)
                
                
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)


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
    projects = Project.objects.filter(owner=request.user)
    
    # count pending, completed and all tasks
    task_count = tasks.count()
    completed_task_count = tasks.filter(completed=True).count()
    pending_task_count = task_count - completed_task_count
    project_count = projects.count()
    completed_project_count = projects.filter(status='Completed').count()
    pending_project_count = projects.filter(status='Pending').count()
    return render(request, 'task/profile.html', {
        'user': user,
        'task_count': task_count,
        'visitor': visitor,
        'task_count': task_count,
        'notifications': notifications,
        'completed_task_count': completed_task_count,
        'pending_task_count': pending_task_count,
        'project_count': project_count,
        'completed_project_count': completed_project_count,
        'pending_project_count': pending_project_count

    })

@csrf_exempt
@login_required
def edit_profile(request):
    user = request.user
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
            return redirect('task:profile', user_id=user.id)
        except Exception as e:
            messages.warning(request, str(e))
            return redirect('task:profile', user_id=user.id)

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
        users = CustomUser.objects.filter(username__icontains=query).values('id', 'username', 'profile_image')
        user_data = []
        for user in users:
            profile_image_url = user['profile_image']
            user_data.append({
                'id': user['id'],
                'username': user['username'],
                'profile_image': profile_image_url
            })
        return JsonResponse({'users': user_data}, status=200)
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

@csrf_exempt
def remove_friend(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if data:
            user_id = data['id']
            friends, created = Friends.objects.get_or_create(user=request.user)
            user = get_object_or_404(CustomUser, id=user_id)
            friends.friends.remove(user)
            Notification.objects.create(user=user, message=f'${request.user} removed you from his friend list!')
            return JsonResponse({'status': 'success'}, status=200)
        else:
            return JsonResponse({'status': 'error'}, status=400)

# Project

def project(request):
    user = request.user
    user_id = user.id
    notifications = Notification.objects.filter(user=user_id, is_read=False).all()
    projects = Project.objects.filter(
        Q(members=user_id) | Q(owner=user_id)
    )  
    form = ProjectForm(owner=user_id)  
    return render(request, 'project/index.html', {
        'notifications': notifications,
        'projects': projects,
        'form':form,
    })


def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, owner=request.user)
        if form.is_valid():
            
            project = form.save(commit=False)
            project.owner = request.user 
            project.save() 
            project.members.add(request.user)  
            form.save_m2m()  

            member_ids = request.POST.getlist('members') 
            for member_id in member_ids:
                user = get_object_or_404(CustomUser, pk=member_id)
                project.members.add(user)  
                Notification.objects.create(
                    user=user,
                    message=f"{request.user} created {project.name} and added you"
                )

            return JsonResponse({
                "project": {
                    "name": project.name,
                    "status": "Pending",
                    "members": project.members.count(),
                    'id': project.id
                }
            }, status=200)
        else:
            return JsonResponse({"errors": form.errors}, status=400)

    # Retourne une réponse non autorisée si ce n'est pas une requête POST
    return JsonResponse({"error": "Invalid request method"}, status=405)

def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    try:
        comments = get_list_or_404(Comment, project=project)
    except:
        comments = None
    form = GroupTaskForm(owner=request.user)
    activities = ProjectActivity.objects.filter(project=project)
    return render(request, 'project/project_detail.html', {
        'project':project,
        'notifications': notifications,
        'comments': comments,
        'form': form,
        'activities': activities
    })

def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    for member in project.members.all():
        Notification.objects.create(user=member, message=f'{request.user} deleted the {project.name} project')
    project.delete()
    messages.warning(request, f'Project  deleted !')
    return redirect('task:project')

@csrf_exempt
def edit_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        data = json.loads(request.body)
        if data:
            try:
                name = data['newName']
            except:
                name = None
            try:
                description = data['description']
            except:
                description = None
            if name:
                project.name = name
                project.save()
                ProjectActivity.objects.create(project=project ,author=request.user, activity=f'changed the project name to {name}')
                return JsonResponse({'message': 'name changed'}, status=200)
            elif description:
                project.description = description
                project.save()
                ProjectActivity.objects.create(project=project ,author=request.user, activity=f'changed the project description to {description}')
                return JsonResponse({'message': 'description changed'}, status=200)
            else:
                return JsonResponse({'error': 'data is none'}, status=400)
        return JsonResponse({'error': 'No data '}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def change_project_status(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'PUT':
        data = json.loads(request.body)
        if data:
            status = data['newStatus']
            project.status = status
            project.save()
            ProjectActivity.objects.create(project=project ,author=request.user, activity=f'change the project status to {status}')
            return JsonResponse({'success': True,'message': 'status changed'}, status=200)
        return JsonResponse({'error': 'no data'}, status=405)
    

    
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
                ProjectActivity.objects.create(project=project ,author=request.user, activity=f'added {user} to the project')
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
                ProjectActivity.objects.create(project=project ,author=request.user, activity=f'removed {user} from the project')
                Notification.objects.create(user=user, sender=request.user, message=f"{request.user}, deleted you from '{project.name}' project")
                return JsonResponse({"message": f" has been removed from the project."}, status=200)
            else:
                return JsonResponse({"error": f"is not a member of the project."}, status=400)
        except CustomUser.DoesNotExist:
            return JsonResponse({"error": f"User  does not exist."}, status=404)

    return JsonResponse({"error": "Invalid request."}, status=400)

@csrf_exempt
def create_project_task(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        form = GroupTaskForm(request.POST, owner=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            ProjectActivity.objects.create(project=project ,author=request.user, activity='created a new task')
            user = CustomUser.objects.get(pk=request.POST.get('assigned_to'))
            Notification.objects.create(user=user, message=f'{request.user} assigned a task to you in the "{project.name}" project')
            return JsonResponse({'message': 'task created successfully'}, status=201)
        return JsonResponse({'error': 'the form is not valid'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def comment(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        if comment_text:
            comment = Comment.objects.create(
                author=request.user,
                project=project,
                comment=comment_text
            )
            return JsonResponse({
                'message': 'Comment added successfully',
                'comment': {
                    'id': comment.id,
                    'author': comment.author.username,
                    'comment': comment.comment,
                    'profile_image': comment.author.profile_image.url if comment.author.profile_image else '',
                    'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
                }
            }, status=200)
        return JsonResponse({'error': 'Comment text is required'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

    
def get_out_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    ProjectActivity.objects.create(project=project ,author=request.user, activity=f' {request.user} gone out of this project')
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


@csrf_exempt
def update_task_category(request):
    data = json.loads(request.body)
    task_id = data.get('task_id')
    new_category = data.get('category')
    
    try:
        task = Task.objects.get(id=task_id)
        task.priority = new_category
        task.save()

        return JsonResponse({'success': True})
    except Task.DoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=404)
    

def focus_mode(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    # Construire les données pour la réponse JSON
    response_data = {
        'task': {
            'id': task.id,
            'title': task.title,
            'description': task.description,  # Si disponible
        },
        'content': render(request, 'task/focus_mode.html', {'task': task}).content.decode('utf-8'),
    }
    return JsonResponse(response_data)
    
