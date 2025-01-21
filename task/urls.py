from django.urls import include, path

from . import views

app_name = 'task'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    
    # User authentication
    path('login', views.login_view, name='login'),
    path('register', views.register_view, name='register'),
    path('logout', views.logout_view, name='logout'),
    
    # Task management
    path('tasks/', views.tasks_view, name='tasks'),
    path('delete_task/<int:task_id>', views.delete_task, name='delete_task'),
    
    # User profile
    path('profile/<int:user_id>', views.profile_view, name='profile'),
    
    # Legal pages
    path('privacy', views.privacy_policy, name='privacy'),
    path('terms', views.terms_and_conditions, name='terms'),
    
    # API Routes
    path('task/<int:task_id>', views.task, name='task'),
    path('tasks/new_task', views.new_task, name='new_task'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('update-task-category/', views.update_task_category, name='update_task_category'),
    path('task/<int:task_id>/focus_mode', views.focus_mode, name='focus_mode'),
    path('task/chart', views.chart, name='chart'),
    
    # Export functionalities
    path('export/csv/', views.export_tasks_csv, name='export_tasks_csv'),
    path('export_pdf/', views.export_to_pdf, name='export_pdf'),
]
