"""coffeeconnect URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('log_coffee/', views.log_coffee, name='log_coffee'),
    path('history/', views.coffee_history, name='coffee_history'),
    
    # Grinder management urls
    path('grinders/', views.manage_grinders, name='manage_grinders'),
    path('grinders/<int:pk>/edit/', views.edit_grinder, name='edit_grinder'),
    path('grinders/<int:pk>/delete/', views.delete_grinder, name='delete_grinder'),
    
    # Analytics API endpoint
    path('api/analytics/', views.get_analytics_data, name='get_analytics_data'),
]
