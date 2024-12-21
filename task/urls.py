from django.urls import path

from . import views

app_name = 'task'
urlpatterns = [

    ## task

    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('register', views.register_view, name='register'),
    path('logout', views.logout_view, name='logout'),
    path('tasks/', views.tasks_view, name='tasks'),
    path('delete_task/<int:task_id>', views.delete_task, name='delete_task'),
    path('profile/<int:user_id>', views.profile_view, name='profile'),
    # API Routes
    path('task/<int:task_id>', views.task, name='task'),
    path('tasks/new_task', views.new_task, name='new_task'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('update-task-category/', views.update_task_category, name='update_task_category'),
    path('task/<int:task_id>/focus_mode', views.focus_mode, name='focus_mode'),
    path('task/chart', views.chart, name='chart'),

 
]
