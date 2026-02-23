from django.contrib import admin
from .models import Topic, Question, Bookmark, CompletedQuestion


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'topic', 'difficulty', 'created_at']
    list_filter = ['topic', 'difficulty']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}


class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'created_at']
    search_fields = ['user__username', 'question__title']


class CompletedQuestionAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'completed_at']
    search_fields = ['user__username', 'question__title']


admin.site.register(Topic, TopicAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Bookmark, BookmarkAdmin)
admin.site.register(CompletedQuestion, CompletedQuestionAdmin)
