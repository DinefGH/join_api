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
from join_backend.views import UserRegistrationView, UserDetailsView, ContactListCreateView, ContactDetailView, CategoryListCreateAPIView, CategoryDetailAPIView, SubtaskListCreateAPIView, SubtaskDetailAPIView, TaskListCreateAPIView, TaskDetailAPIView




urlpatterns = [
    path('set-csrf/', set_csrf_token, name='set-csrf'),
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', UserRegistrationView.as_view(), name='user-register'),
    path('user/details/', UserDetailsView.as_view(), name='user-details'),
    path('addcontact/',ContactListCreateView.as_view(), name='add_contact'),
    path('contact/<int:id>/', ContactDetailView.as_view(), name='contact_detail'),
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailAPIView.as_view(), name='category-detail'),
    path('subtasks/', SubtaskListCreateAPIView.as_view(), name='subtask-list'),
    path('subtasks/<int:pk>/', SubtaskDetailAPIView.as_view(), name='subtask-detail'),
    path('tasks/', TaskListCreateAPIView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskDetailAPIView.as_view(), name='task-detail'),
]
