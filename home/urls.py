from django.urls import path

from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home_view, name="home"),
    path('u/<str:username>/', views.user_profile_view, name="user_profile"),
    path('create/', views.create_post_view, name="create_post"),
    path('edit/<str:pk>/', views.update_post_view, name="update_post"),
    path('d/<str:pk>/', views.delete_post_view, name="delete_post"),

    path('explore/', views.explore_view, name="explore"),
    path('p/<str:pk>/', views.post_view, name="post"),
    path('saved/', views.saved_post_view, name="saved_post"),
    
    path('features', views.features_views, name="features"),
]