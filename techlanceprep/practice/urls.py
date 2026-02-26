from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_topics, name='all_topics'),
    path('topic/<slug:slug>/', views.topic_questions, name='topic_questions'),
    path('question/<slug:topic_slug>/<slug:slug>/', views.question_detail, name='question_detail'),
    path('bookmarks/', views.bookmark_list, name='bookmark_list'),
    path('api/toggle-bookmark/', views.toggle_bookmark, name='toggle_bookmark'),
    path('api/toggle-complete/', views.toggle_complete, name='toggle_complete'),
]
