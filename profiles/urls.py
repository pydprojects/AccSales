"""TestTask URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.base, name='base')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='base')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from . import views

app_name = 'profiles'
urlpatterns = [
    path('login/', views.LogIn.as_view(), name='login'),
    path('logout/', views.LogOut.as_view(), name='logout'),
    path('register/', views.Register.as_view(), name='register'),
    path('confirm/<slug:uidb64>/<slug:token>/', views.Confirm.as_view(), name='confirm'),
    path('resend-confirmation/<str:username>/', views.ResendConfirmation.as_view(), name='resend-confirmation'),
    path('self/<str:username>/', views.Profile.as_view(), name='profile'),
    path('edit/', views.ProfileEdit.as_view(), name='profile-edit'),
]
