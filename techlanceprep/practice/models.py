from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model


class Topic(models.Model):
    TOPIC_TYPE_CHOICES = [
        ('coding', 'Coding'),
        ('technical', 'Technical'),
        ('hr', 'HR'),
    ]
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='📚')
    topic_type = models.CharField(max_length=20, choices=TOPIC_TYPE_CHOICES, default='coding')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('topic_questions', kwargs={'slug': self.slug})


class Question(models.Model):
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]
    
    QUESTION_TYPE_CHOICES = [
        ('coding', 'Coding'),
        ('technical', 'Technical'),
        ('hr', 'HR'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    solution = models.TextField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='questions')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='Easy')
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES, default='coding')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('question_detail', kwargs={
            'topic_slug': self.topic.slug,
            'slug': self.slug
        })


class Bookmark(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='bookmarks')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'question']
    
    def __str__(self):
        return f"{self.user.username} - {self.question.title}"


class CompletedQuestion(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='completed_questions')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='completed_by')
    completed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'question']
    
    def __str__(self):
        return f"{self.user.username} - {self.question.title}"
    

