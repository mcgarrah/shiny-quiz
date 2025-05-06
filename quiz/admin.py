from django.contrib import admin
from .models import (
    Category, Quiz, Question, Answer, 
    Sitting, Progress, EssayQuestion, EssayAnswer
)

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4
    max_num = 10

class EssayQuestionInline(admin.StackedInline):
    model = EssayQuestion
    max_num = 1

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'quiz', 'question_type', 'created_at']
    list_filter = ['quiz', 'question_type', 'created_at']
    search_fields = ['text', 'quiz__title']
    inlines = [AnswerInline, EssayQuestionInline]
    
    def get_inline_instances(self, request, obj=None):
        """Only show relevant inlines based on question type"""
        inlines = []
        if obj:
            if obj.question_type in ['multiple_choice', 'true_false']:
                inlines.append(self.inlines[0](self.model, self.admin_site))
            elif obj.question_type == 'essay':
                inlines.append(self.inlines[1](self.model, self.admin_site))
        return inlines

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    show_change_link = True
    fields = ['text', 'question_type']

class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'created_by', 'created_at', 'draft', 'question_count']
    list_filter = ['category', 'created_by', 'draft', 'created_at']
    search_fields = ['title', 'description', 'category__name', 'created_by__username']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [QuestionInline]
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'category', 'created_by')
        }),
        ('Quiz Settings', {
            'fields': ('random_order', 'max_questions', 'answers_at_end', 'exam_paper', 
                      'single_attempt', 'pass_mark', 'time_limit', 'draft')
        }),
        ('Messages', {
            'fields': ('success_text', 'fail_text')
        }),
    )
    
    def question_count(self, obj):
        return obj.questions.count()
    question_count.short_description = 'Questions'

class SittingAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'current_score', 'complete', 'start_time', 'end_time']
    list_filter = ['quiz', 'complete', 'start_time']
    search_fields = ['user__username', 'quiz__title']
    readonly_fields = ['question_order', 'question_list', 'incorrect_questions', 'user_answers']
    
    def has_add_permission(self, request):
        return False

class ProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'score', 'correct_answers', 'total_questions', 'created_at']
    list_filter = ['quiz', 'created_at']
    search_fields = ['user__username', 'quiz__title']
    
    def has_add_permission(self, request):
        return False

class EssayAnswerAdmin(admin.ModelAdmin):
    list_display = ['sitting', 'question', 'is_correct']
    list_filter = ['is_correct', 'sitting__quiz']
    search_fields = ['sitting__user__username', 'question__text']
    fields = ['sitting', 'question', 'answer', 'is_correct', 'comments']
    readonly_fields = ['sitting', 'question', 'answer']

admin.site.register(Category)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Sitting, SittingAdmin)
admin.site.register(Progress, ProgressAdmin)
admin.site.register(EssayAnswer, EssayAnswerAdmin)