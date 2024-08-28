from django.contrib import admin
from .models import Course, Chapter, Quiz, Question, Enrollment

admin.site.register(Course)
admin.site.register(Chapter)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Enrollment)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'quiz', 'correct_option')
    list_filter = ('quiz',)
    search_fields = ('question_text',)
    ordering = ('quiz',)