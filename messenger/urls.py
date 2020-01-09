"""URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = 'messenger'

urlpatterns = [
    path('dialogs/', login_required(views.DialogsView.as_view()), name='dialogs'),
    # path('dialogs/create/<int:user_id>/', 'login_required(views.CreateDialogView.as_view())', name='create_dialog'),
    path('dialogs/<int:chat_id>/', login_required(views.MessagesView.as_view()), name='messages'),
]
