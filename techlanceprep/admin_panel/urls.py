from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    
    # Topics CRUD
    path('topics/', views.manage_topics, name='manage_topics'),
    path('topics/add/', views.add_topic, name='add_topic'),
    path('topics/edit/<int:topic_id>/', views.edit_topic, name='edit_topic'),
    path('topics/delete/<int:topic_id>/', views.delete_topic, name='delete_topic'),
    
    # Questions CRUD
    path('questions/', views.manage_questions, name='manage_questions'),
    path('questions/add/', views.add_question, name='add_question'),
    path('questions/edit/<int:question_id>/', views.edit_question, name='edit_question'),
    path('questions/delete/<int:question_id>/', views.delete_question, name='delete_question'),
    
    # Users
    path('users/', views.manage_users, name='manage_users'),
    path('users/view/<int:user_id>/', views.view_user, name='view_user'),
    path('users/toggle-admin/<int:user_id>/', views.toggle_user_admin, name='toggle_user_admin'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    
    # Bookmarks & Completions
    path('bookmarks/', views.manage_bookmarks, name='manage_bookmarks'),
    path('completions/', views.manage_completions, name='manage_completions'),
]

