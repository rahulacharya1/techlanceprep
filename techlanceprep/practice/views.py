from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Topic, Question, Bookmark, CompletedQuestion


def home(request):
    topics = Topic.objects.all()
    total_questions = Question.objects.count()
    return render(request, 'core/home.html', {
        'topics': topics,
        'total_questions': total_questions,
    })


def all_questions(request):
    questions = Question.objects.all().order_by('-created_at')
    topics = Topic.objects.all()
    
    # Filters
    topic_slug = request.GET.get('topic')
    difficulty = request.GET.get('difficulty')
    
    if topic_slug:
        questions = questions.filter(topic__slug=topic_slug)
    if difficulty:
        questions = questions.filter(difficulty=difficulty)
    
    # Check bookmarks and completed for logged in user
    bookmark_ids = []
    completed_ids = []
    if request.user.is_authenticated:
        bookmark_ids = Bookmark.objects.filter(user=request.user).values_list('question_id', flat=True)
        completed_ids = CompletedQuestion.objects.filter(user=request.user).values_list('question_id', flat=True)
    
    return render(request, 'practice/question_list.html', {
        'questions': questions,
        'topics': topics,
        'selected_topic': topic_slug,
        'selected_difficulty': difficulty,
        'bookmark_ids': list(bookmark_ids),
        'completed_ids': list(completed_ids),
    })


def topic_questions(request, slug):
    topic = get_object_or_404(Topic, slug=slug)
    questions = topic.questions.all().order_by('-created_at')
    topics = Topic.objects.all()
    
    # Check bookmarks and completed for logged in user
    bookmark_ids = []
    completed_ids = []
    if request.user.is_authenticated:
        bookmark_ids = Bookmark.objects.filter(user=request.user).values_list('question_id', flat=True)
        completed_ids = CompletedQuestion.objects.filter(user=request.user).values_list('question_id', flat=True)
    
    return render(request, 'practice/question_list.html', {
        'questions': questions,
        'topics': topics,
        'selected_topic': slug,
        'current_topic': topic,
        'bookmark_ids': list(bookmark_ids),
        'completed_ids': list(completed_ids),
    })


def question_detail(request, topic_slug, slug):
    question = get_object_or_404(Question, topic__slug=topic_slug, slug=slug)
    
    is_bookmarked = False
    is_completed = False
    
    if request.user.is_authenticated:
        is_bookmarked = Bookmark.objects.filter(user=request.user, question=question).exists()
        is_completed = CompletedQuestion.objects.filter(user=request.user, question=question).exists()
    
    return render(request, 'practice/question_detail.html', {
        'question': question,
        'is_bookmarked': is_bookmarked,
        'is_completed': is_completed,
    })


@login_required
@require_POST
def toggle_bookmark(request):
    question_id = request.POST.get('question_id')
    question = get_object_or_404(Question, id=question_id)
    
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, question=question)
    
    if not created:
        bookmark.delete()
        return JsonResponse({'status': 'removed', 'message': 'Bookmark removed'})
    else:
        return JsonResponse({'status': 'added', 'message': 'Bookmark added'})


@login_required
@require_POST
def toggle_complete(request):
    question_id = request.POST.get('question_id')
    question = get_object_or_404(Question, id=question_id)
    
    completed, created = CompletedQuestion.objects.get_or_create(user=request.user, question=question)
    
    if not created:
        completed.delete()
        return JsonResponse({'status': 'removed', 'message': 'Marked as incomplete'})
    else:
        return JsonResponse({'status': 'added', 'message': 'Marked as completed'})


@login_required
def bookmark_list(request):
    bookmarks = Bookmark.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'practice/bookmark_list.html', {'bookmarks': bookmarks})

