from django.shortcuts import render
from practice.models import Topic, Question


def home(request):
    topics = Topic.objects.all()
    total_questions = Question.objects.count()
    return render(request, 'core/home.html', {
        'topics': topics,
        'total_questions': total_questions,
    })


def about(request):
    return render(request, 'core/about.html')


def contact(request):
    return render(request, 'core/contact.html')
