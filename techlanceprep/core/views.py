from django.shortcuts import render
from practice.models import Topic, Question
from accounts.models import User


def home(request):
    topics = Topic.objects.all()
    total_questions = Question.objects.count()
    user = User.objects.all()
    return render(request, 'core/home.html', {
        'topics': topics,
        'total_questions': total_questions,
        'user': user
    })


def about(request):
    return render(request, 'core/about.html')


def contact(request):
    return render(request, 'core/contact.html')


def privacy_policy(request):
    return render(request, 'core/privacy_policy.html')


def terms_of_service(request):
    return render(request, 'core/terms_of_service.html')

