from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('users/', views.manage_users, name='manage_users'),
    path('users/toggle-admin/<int:user_id>/', views.toggle_user_admin, name='toggle_user_admin'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('topics/', views.manage_topics, name='manage_topics'),
    path('questions/', views.manage_questions, name='manage_questions'),
]

