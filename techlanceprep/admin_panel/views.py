from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Q
from accounts.models import User
from practice.models import Topic, Question, Bookmark, CompletedQuestion
from django.utils import timezone


# Check if user is admin
def is_admin(user):
    return user.is_admin or user.is_superuser


def admin_login(request):
    """Custom admin login page"""
    if request.user.is_authenticated:
        if is_admin(request.user):
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'You do not have admin access')
            return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        from django.contrib.auth import authenticate
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            if is_admin(user):
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'You do not have admin access')
        else:
            messages.error(request, 'Invalid email or password')
    
    return render(request, 'admin_panel/login.html')


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Main admin dashboard"""
    # User stats
    total_users = User.objects.count()
    today = timezone.now().date()
    new_users_today = User.objects.filter(date_joined__date=today).count()
    
    # Question stats
    total_questions = Question.objects.count()
    total_topics = Topic.objects.count()
    
    # Activity stats
    total_bookmarks = Bookmark.objects.count()
    total_completions = CompletedQuestion.objects.count()
    
    # Recent activity
    recent_users = User.objects.order_by('-date_joined')[:5]
    recent_questions = Question.objects.order_by('-created_at')[:5]
    
    # Difficulty breakdown
    easy_count = Question.objects.filter(difficulty='Easy').count()
    medium_count = Question.objects.filter(difficulty='Medium').count()
    hard_count = Question.objects.filter(difficulty='Hard').count()
    
    # Type breakdown
    coding_count = Question.objects.filter(question_type='coding').count()
    technical_count = Question.objects.filter(question_type='technical').count()
    hr_count = Question.objects.filter(question_type='hr').count()
    
    context = {
        'total_users': total_users,
        'new_users_today': new_users_today,
        'total_questions': total_questions,
        'total_topics': total_topics,
        'total_bookmarks': total_bookmarks,
        'total_completions': total_completions,
        'recent_users': recent_users,
        'recent_questions': recent_questions,
        'easy_count': easy_count,
        'medium_count': medium_count,
        'hard_count': hard_count,
        'coding_count': coding_count,
        'technical_count': technical_count,
        'hr_count': hr_count,
    }
    
    return render(request, 'admin_panel/dashboard.html', context)


# ==================== TOPIC MANAGEMENT ====================

@login_required
@user_passes_test(is_admin)
def manage_topics(request):
    """Manage all topics"""
    topics = Topic.objects.annotate(question_count=Count('questions')).order_by('name')
    return render(request, 'admin_panel/topics.html', {'topics': topics})


@login_required
@user_passes_test(is_admin)
def add_topic(request):
    """Add new topic"""
    if request.method == 'POST':
        name = request.POST.get('name')
        icon = request.POST.get('icon')
        description = request.POST.get('description')
        
        topic = Topic.objects.create(
            name=name,
            icon=icon,
            description=description,
        )
        messages.success(request, f'Topic "{topic.name}" created successfully!')
        return redirect('manage_topics')
    
    return render(request, 'admin_panel/topic_form.html', {'topic': None, 'action': 'Add'})


@login_required
@user_passes_test(is_admin)
def edit_topic(request, topic_id):
    """Edit existing topic"""
    topic = get_object_or_404(Topic, id=topic_id)
    
    if request.method == 'POST':
        topic.name = request.POST.get('name')
        topic.icon = request.POST.get('icon')
        topic.description = request.POST.get('description')
        topic.topic_type = request.POST.get('topic_type')
        topic.save()
        messages.success(request, f'Topic "{topic.name}" updated successfully!')
        return redirect('manage_topics')
    
    return render(request, 'admin_panel/topic_form.html', {'topic': topic, 'action': 'Edit'})


@login_required
@user_passes_test(is_admin)
def delete_topic(request, topic_id):
    """Delete a topic"""
    topic = get_object_or_404(Topic, id=topic_id)
    topic_name = topic.name
    
    # Delete all questions under this topic first
    question_count = topic.questions.count()
    if question_count > 0:
        topic.questions.all().delete()
    
    topic.delete()
    messages.success(request, f'Topic "{topic_name}" and {question_count} questions deleted!')
    return redirect('manage_topics')


# ==================== QUESTION MANAGEMENT ====================

@login_required
@user_passes_test(is_admin)
def manage_questions(request):
    """Manage all questions"""
    questions = Question.objects.select_related('topic').order_by('-created_at')
    
    # Filters
    topic_filter = request.GET.get('topic')
    difficulty_filter = request.GET.get('difficulty')
    type_filter = request.GET.get('type')
    
    if topic_filter:
        questions = questions.filter(topic__slug=topic_filter)
    if difficulty_filter:
        questions = questions.filter(difficulty=difficulty_filter)
    if type_filter:
        questions = questions.filter(question_type=type_filter)
    
    topics = Topic.objects.all()
    
    return render(request, 'admin_panel/questions.html', {
        'questions': questions,
        'topics': topics,
        'topic_filter': topic_filter,
        'difficulty_filter': difficulty_filter,
        'type_filter': type_filter,
    })


@login_required
@user_passes_test(is_admin)
def add_question(request):
    """Add new question"""
    topics = Topic.objects.all()
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        solution = request.POST.get('solution')
        topic_id = request.POST.get('topic')
        difficulty = request.POST.get('difficulty')
        question_type = request.POST.get('question_type')
        
        topic = get_object_or_404(Topic, id=topic_id)
        
        question = Question.objects.create(
            title=title,
            description=description,
            solution=solution,
            topic=topic,
            difficulty=difficulty,
            question_type=question_type
        )
        messages.success(request, f'Question "{question.title}" created successfully!')
        return redirect('manage_questions')
    
    return render(request, 'admin_panel/question_form.html', {'question': None, 'topics': topics, 'action': 'Add'})


@login_required
@user_passes_test(is_admin)
def edit_question(request, question_id):
    """Edit existing question"""
    question = get_object_or_404(Question, id=question_id)
    topics = Topic.objects.all()
    
    if request.method == 'POST':
        question.title = request.POST.get('title')
        question.description = request.POST.get('description')
        question.solution = request.POST.get('solution')
        question.topic = get_object_or_404(Topic, id=request.POST.get('topic'))
        question.difficulty = request.POST.get('difficulty')
        question.question_type = request.POST.get('question_type')
        question.save()
        messages.success(request, f'Question "{question.title}" updated successfully!')
        return redirect('manage_questions')
    
    return render(request, 'admin_panel/question_form.html', {
        'question': question,
        'topics': topics,
        'action': 'Edit'
    })


@login_required
@user_passes_test(is_admin)
def delete_question(request, question_id):
    """Delete a question"""
    question = get_object_or_404(Question, id=question_id)
    question_title = question.title
    question.delete()
    messages.success(request, f'Question "{question_title}" deleted!')
    return redirect('manage_questions')


# ==================== USER MANAGEMENT ====================

@login_required
@user_passes_test(is_admin)
def manage_users(request):
    """Manage all users"""
    users = User.objects.all().order_by('-date_joined')
    
    # Search
    search = request.GET.get('search')
    if search:
        users = users.filter(
            Q(username__icontains=search) | 
            Q(email__icontains=search)
        )
    
    return render(request, 'admin_panel/users.html', {'users': users})


@login_required
@user_passes_test(is_admin)
def view_user(request, user_id):
    """View user details with their bookmarks and completions"""
    user = get_object_or_404(User, id=user_id)
    bookmarks = Bookmark.objects.filter(user=user).select_related('question__topic')
    completions = CompletedQuestion.objects.filter(user=user).select_related('question__topic')
    
    return render(request, 'admin_panel/user_detail.html', {
        'view_user': user,
        'bookmarks': bookmarks,
        'completions': completions,
    })


@login_required
@user_passes_test(is_admin)
def toggle_user_admin(request, user_id):
    """Toggle admin status of a user"""
    if not request.user.is_superuser:
        messages.error(request, 'Only superusers can perform this action')
        return redirect('manage_users')
    
    user = get_object_or_404(User, id=user_id)
    user.is_admin = not user.is_admin
    user.save()
    
    if user.is_admin:
        messages.success(request, f'{user.username} is now an Admin!')
    else:
        messages.success(request, f'{user.username} is no longer an Admin!')
    
    return redirect('manage_users')


@login_required
@user_passes_test(is_admin)
def delete_user(request, user_id):
    """Delete a user"""
    if not request.user.is_superuser:
        messages.error(request, 'Only superusers can perform this action')
        return redirect('manage_users')
    
    user = get_object_or_404(User, id=user_id)
    if user == request.user:
        messages.error(request, 'You cannot delete yourself!')
    else:
        username = user.username
        user.delete()
        messages.success(request, f'User "{username}" deleted successfully!')
    
    return redirect('manage_users')


# ==================== BOOKMARKS & COMPLETIONS ====================

@login_required
@user_passes_test(is_admin)
def manage_bookmarks(request):
    """View all bookmarks"""
    bookmarks = Bookmark.objects.select_related('user', 'question__topic').order_by('-created_at')
    
    # Filter by user
    user_id = request.GET.get('user')
    if user_id:
        bookmarks = bookmarks.filter(user_id=user_id)
    
    return render(request, 'admin_panel/all_bookmarks.html', {'bookmarks': bookmarks})


@login_required
@user_passes_test(is_admin)
def manage_completions(request):
    """View all completions"""
    completions = CompletedQuestion.objects.select_related('user', 'question__topic').order_by('-completed_at')
    
    # Filter by user
    user_id = request.GET.get('user')
    if user_id:
        completions = completions.filter(user_id=user_id)
    
    return render(request, 'admin_panel/all_completions.html', {'completions': completions})


@login_required
@user_passes_test(is_admin)
def admin_logout(request):
    """Admin logout"""
    logout(request)
    messages.info(request, 'You have been logged out from admin panel')
    return redirect('admin_login')

