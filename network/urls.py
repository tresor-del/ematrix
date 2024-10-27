
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new post", views.new_post, name="new_post"),
    path("following", views.following, name="following"),
    path("user/<str:user_profile>", views.profile_page, name="profile_page"),

    # API'S URLS
    
    path("likes/<int:id>", views.like_posts, name="likes"),
    path('edit/<int:id>', views.edit_post, name="edit_post"),

]
