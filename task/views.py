import json
import csv
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_list_or_404, redirect, render, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime
from django.contrib import messages

from .forms import TaskForm
from .models import CustomUser, Task


from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from django.http import HttpResponse

def export_to_pdf(request):

    # Créer une réponse HTTP avec un type de contenu PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="tasks.pdf"'

    # Créer un objet canvas pour le PDF
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Exemple de contenu
    tasks = Task.objects.filter(author=request.user)

    # Ajouter du texte au PDF avec des couleurs
    y = height - 50  # Position verticale
    p.setFont("Helvetica-Bold", 16)
    p.setFillColor(colors.darkblue)
    p.drawString(100, y, f"Task Lists for {request.user}:")
    y -= 30

    p.setFont("Helvetica", 12)
    for task in tasks:
        p.setFillColor(colors.black)
        p.drawString(100, y, "Title:")
        p.setFillColor(colors.green)
        p.drawString(150, y, task.title)
        y -= 20

        p.setFillColor(colors.black)
        p.drawString(100, y, "Priority:")
        p.setFillColor(colors.red)
        p.drawString(150, y, task.priority)
        y -= 20

        p.setFillColor(colors.black)
        p.drawString(100, y, "Creation Date:")
        p.setFillColor(colors.blue)
        p.drawString(200, y, task.created_at.strftime('%Y-%m-%d'))
        y -= 40

    # Sauvegarder et fermer le PDF
    p.showPage()
    p.save()

    return response


def export_tasks_csv(request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tasks.csv"'

    writer = csv.writer(response)
    writer.writerow(['Title', 'Priorité', 'Creation date'])  # Header
    tasks = Task.objects.filter(author=request.user)

    for task in tasks:
        writer.writerow([task.title, task.priority, task.created_at])

    return response


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
            return render(request, 'account/login.html', {
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
            return render(request, 'account/register.html', {
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
            return render(request, 'account/signup.html', {
                'message': str(e)
            })
    
    return render(request, 'task/signup.html')



def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('task:index'))

#Tasks views

def tasks_view(request):
    today = datetime.today().date()
    tasks = Task.objects.filter(author=request.user, due_date=today)
    tasks_count = tasks.count()
    completed_task_count = tasks.filter(completed=True).count()
    pending_task_count = tasks_count - completed_task_count 

    important_urgent_tasks = tasks.filter(priority='important and urgent')
    important_not_urgent_tasks = tasks.filter(priority='important but not urgent')
    not_important_urgent_tasks = tasks.filter(priority='not important but ugent')
    not_important_not_urgent_tasks = tasks.filter(priority='not important and not urgent')

    return render(request, 'task/tasks.html', {
        'today': today,
        'tasks': tasks,
        'completed_task_count' : completed_task_count,
        'pending_task_count' : pending_task_count,
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

#Profile views

def profile_view(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    visitor = request.user
    tasks = Task.objects.filter(author=request.user, )
    # count pending, completed and all tasks
    task_count = tasks.count()
    completed_task_count = tasks.filter(completed=True).count()
    pending_task_count = task_count - completed_task_count
    return render(request, 'task/profile.html', {
        'user': user,
        'task_count': task_count,
        'visitor': visitor,
        'task_count': task_count,
        'completed_task_count': completed_task_count,
        'pending_task_count': pending_task_count,
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
            return redirect('task:tasks', user_id=user.id)
        except Exception as e:
            messages.warning(request, str(e))
            return redirect('task:tasks')

    return render(request, 'task/edit_profile.html', {
        'user': request.user,
        })



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

def chart(request):
    today = datetime.today().date()
    tasks = Task.objects.filter(author=request.user, due_date=today)
    tasks_count = tasks.count()
    completed_task_count = tasks.filter(completed=True).count()
    pending_task_count = tasks_count - completed_task_count 
    return render(request, 'task/chart.html', {
        'completed_task_count' : completed_task_count,
        'pending_task_count' : pending_task_count
    })

def privacy_policy(request):
    return render(request, 'task/privacy.html')

def terms_and_conditions(request):
    return render(request, 'task/terms.html')
    
