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
    path('calendar_tasks/<str:due_date>', views.calendar_tasks, name='calendar_tasks'),
    path('profile/<int:user_id>', views.profile_view, name='profile'),
    # API Routes
    path('task/<int:task_id>', views.task, name='task'),
    path('tasks/new_task', views.new_task, name='new_task'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('update-task-category/', views.update_task_category, name='update_task_category'),
    path('task/<int:task_id>/focus_mode', views.focus_mode, name='focus_mode'),

    # Notifications

    path('notifications', views.notifications, name='notifications'),
    # API Routes
    path('delete_notification/<int:notification_id>', views.delete_notification, name='delete_notification'),
    path('delete_all_notification', views.delete_all_notification, name='delete_all_notification'),


    #Collaboration

    path('collaborators', views.collaborators_views, name='collaboration'),
    # API Routes
    path('collaborations/search_users', views.search_users, name='search_user'),
    path('invite_user/<int:user_id>', views.invite_user, name='invite_user'),
    path('remove_friend/', views.remove_friend, name='remove_friend'),
    path('confirm_invitation/<int:user_id>', views.confirm_invitation, name='confirm_invitation'),

    #Project

    path('project', views.project, name='project'),
    path('project/project_detail/<int:project_id>', views.project_detail, name='project_detail'),
    path('project/delete_project/<int:project_id>', views.delete_project, name='delete_project'),
    path('project/edit_project/<int:project_id>', views.edit_project, name='edit_project'),
    path('project/search_members/', views.search_members, name='search_member'),
    path('project/<int:project_id>/add_member/', views.add_member, name='add_member'),
    path('project/<int:project_id>/remove_member/', views.remove_member, name='remove_member'),
    path('project/<int:project_id>/new_task/', views.create_project_task, name='new_project_task'),
    path('project/<int:project_id>/new_comment', views.comment, name='comment'),
    path('project/<int:project_id>/get_out', views.get_out_project, name='get_out_project'),
    path('project/change-status/<int:project_id>', views.change_project_status, name='change-project-status'),
    #API routes
    path('project/create_project', views.create_project, name='create_project'),
    path('project/<int:project_id>/task/<int:task_id>/status', views.change_status, name='change_status'),
]
