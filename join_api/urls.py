"""join_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from join_backend.views import set_csrf_token
from join_backend.views import LoginView
from join_backend.views import UserRegistrationView, UserDetailsView, ContactListCreateView



urlpatterns = [
    path('set-csrf/', set_csrf_token, name='set-csrf'),
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', UserRegistrationView.as_view(), name='user-register'),
    path('user/details/', UserDetailsView.as_view(), name='user-details'),
    path('addcontact/',ContactListCreateView.as_view(), name='add_contact'),

]
