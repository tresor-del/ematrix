from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("Categories", views.categories, name="categories"),
    path("<str:slug>/add_to_watchlist", views.add_to_watchlist, name="add_to_watchlist"),
    path("<str:slug>/Delete_from_watchlist", views.delete_from_watchlist, name="delete_from_watchlist"),
    path("create_listing", views.create_listing, name="listing"),
    path("<str:name>/profile", views.profile, name="profile"),
    path("<str:slug>", views.listing_views, name='listingv'),
    path("<str:category>/active_listing", views.category_active_listing, name='category_active_listing'),

]
