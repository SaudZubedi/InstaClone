from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('register/', views.registration_view, name="register"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),

    path('edit/', views.settings_view, name="settings"),

]