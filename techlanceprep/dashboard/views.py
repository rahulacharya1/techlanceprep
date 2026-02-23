from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from practice.models import Question, Bookmark, CompletedQuestion, Topic


@login_required
def dashboard(request):
    # Basic Stats
    total_questions = Question.objects.count()
    completed_count = CompletedQuestion.objects.filter(user=request.user).count()
    bookmark_count = Bookmark.objects.filter(user=request.user).count()
    
    # Progress Calculation
    progress = 0
    if total_questions > 0:
        progress = (completed_count / total_questions) * 100
    
    # Recent Activity
    recent_completed = CompletedQuestion.objects.filter(user=request.user).order_by('-completed_at')[:5]
    recent_bookmarks = Bookmark.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    # Topic-wise Progress
    topics_progress = []
    for topic in Topic.objects.all():
        topic_total = topic.questions.count()
        topic_completed = CompletedQuestion.objects.filter(
            user=request.user,
            question__topic=topic
        ).count()
        
        if topic_total > 0:
            topic_percent = (topic_completed / topic_total) * 100
        else:
            topic_percent = 0
            
        topics_progress.append({
            'topic': topic,
            'total': topic_total,
            'completed': topic_completed,
            'percent': round(topic_percent, 1)
        })
    
    # Difficulty-wise Progress
    difficulty_stats = {}
    for diff in ['Easy', 'Medium', 'Hard']:
        total = Question.objects.filter(difficulty=diff).count()
        completed = CompletedQuestion.objects.filter(
            user=request.user,
            question__difficulty=diff
        ).count()
        difficulty_stats[diff] = {
            'total': total,
            'completed': completed,
            'percent': round((completed / total * 100), 1) if total > 0 else 0
        }
    
    return render(request, 'dashboard/dashboard.html', {
        'total_questions': total_questions,
        'completed_count': completed_count,
        'bookmark_count': bookmark_count,
        'progress': round(progress, 1),
        'recent_completed': recent_completed,
        'recent_bookmarks': recent_bookmarks,
        'topics_progress': topics_progress,
        'difficulty_stats': difficulty_stats,
    })
    
    
    
    