from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count
from django.utils import timezone
from accounts.models import User
from practice.models import Topic, Question, Bookmark, CompletedQuestion


# Check if user is admin (can access custom admin panel)
def can_access_admin(user):
    return user.is_admin or user.is_superuser or user.is_staff


def admin_login(request):
    """Custom admin login page"""
    # If already logged in and is admin, redirect to admin dashboard
    if request.user.is_authenticated:
        # Check using hasattr to avoid AttributeError
        if hasattr(request.user, 'is_admin') and (request.user.is_admin or request.user.is_superuser or request.user.is_staff):
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
            # Check using hasattr to avoid AttributeError
            if hasattr(user, 'is_admin') and (user.is_admin or user.is_superuser or user.is_staff):
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'You do not have admin access')
                # Still redirect regular users to their dashboard
                login(request, user)
                messages.info(request, 'You do not have admin access. Redirecting to user dashboard.')
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    
    return render(request, 'admin_panel/login.html')


@login_required
@user_passes_test(can_access_admin)
def admin_dashboard(request):
    """Main admin dashboard"""
    # Get today's date properly
    today = timezone.now().date()
    
    # User stats
    total_users = User.objects.count()
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
    }
    
    return render(request, 'admin_panel/dashboard.html', context)


@login_required
@user_passes_test(can_access_admin)
def manage_users(request):
    """Manage all users"""
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'admin_panel/users.html', {'users': users})


@login_required
@user_passes_test(can_access_admin)
def toggle_user_admin(request, user_id):
    """Toggle admin status of a user"""
    if not request.user.is_superuser:
        messages.error(request, 'Only superusers can perform this action')
        return redirect('manage_users')
    
    user = get_object_or_404(User, id=user_id)
    user.is_admin = not user.is_admin
    user.save()
    messages.success(request, f'Admin status updated for {user.username}')
    return redirect('manage_users')


@login_required
@user_passes_test(can_access_admin)
def delete_user(request, user_id):
    """Delete a user"""
    if not request.user.is_superuser:
        messages.error(request, 'Only superusers can perform this action')
        return redirect('manage_users')
    
    user = get_object_or_404(User, id=user_id)
    if user == request.user:
        messages.error(request, 'You cannot delete yourself')
    else:
        user.delete()
        messages.success(request, 'User deleted successfully')
    return redirect('manage_users')


@login_required
@user_passes_test(can_access_admin)
def manage_topics(request):
    """Manage topics"""
    topics = Topic.objects.annotate(question_count=Count('questions'))
    return render(request, 'admin_panel/topics.html', {'topics': topics})


@login_required
@user_passes_test(can_access_admin)
def manage_questions(request):
    """Manage all questions"""
    questions = Question.objects.select_related('topic').order_by('-created_at')
    return render(request, 'admin_panel/questions.html', {'questions': questions})


@login_required
@user_passes_test(can_access_admin)
def admin_logout(request):
    """Admin logout"""
    logout(request)
    messages.info(request, 'You have been logged out from admin panel')
    return redirect('home')