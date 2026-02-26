from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Topic, Question, Bookmark, CompletedQuestion


def home(request):
    return redirect('all_topics')


def all_topics(request):
    all_topics = Topic.objects.all().order_by('name')
    return render(request, 'practice/all_topics.html', {
        'all_topics': all_topics,
    })


def topic_questions(request, slug):
    topic = get_object_or_404(Topic, slug=slug)
    
    all_questions = topic.questions.all()
    
    coding_questions = all_questions.filter(question_type='coding')
    technical_questions = all_questions.filter(question_type='technical')
    hr_questions = all_questions.filter(question_type='hr')
    
    def group_by_difficulty(questions):
        return {
            'Easy': questions.filter(difficulty='Easy').order_by('title'),
            'Medium': questions.filter(difficulty='Medium').order_by('title'),
            'Hard': questions.filter(difficulty='Hard').order_by('title'),
        }
    
    coding = group_by_difficulty(coding_questions)
    technical = group_by_difficulty(technical_questions)
    hr = group_by_difficulty(hr_questions)
    
    bookmark_ids = []
    completed_ids = []
    if request.user.is_authenticated:
        bookmark_ids = list(Bookmark.objects.filter(user=request.user).values_list('question_id', flat=True))
        completed_ids = list(CompletedQuestion.objects.filter(user=request.user).values_list('question_id', flat=True))
    
    return render(request, 'practice/topic_questions.html', {
        'topic': topic,
        'coding': coding,
        'technical': technical,
        'hr': hr,
        'bookmark_ids': bookmark_ids,
        'completed_ids': completed_ids,
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

