"""InstaClone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from os import name
from django.urls.conf import include
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('home.urls')),
    
    path('account/', include('account.urls')),
    


    path('account/password_reset/',
    auth_views.PasswordResetView.as_view(),
    name='password_reset'),

    path('account/reset/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(),
    name='password_reset_confirm'),

    path('account/password_reset/done/',
    auth_views.PasswordResetDoneView.as_view(),
    name='password_reset_done'),

    path('account/reset/done/',
    auth_views.PasswordResetCompleteView.as_view(),
    name='password_reset_complete'),



    path('edit/change_password/',
    auth_views.PasswordChangeView.as_view(),
    name="password_change" ),

    path('edit/change_password/done',
    auth_views.PasswordChangeDoneView.as_view(),
    name='password_change_done'),

]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)