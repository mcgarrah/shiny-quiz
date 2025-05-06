from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    # Quiz listing and details
    path('', views.quiz_list, name='quiz_list'),
    path('quiz/<slug:slug>/', views.quiz_detail, name='quiz_detail'),
    path('quiz/<slug:slug>/take/', views.take_quiz, name='take_quiz'),
    path('results/<int:sitting_id>/', views.quiz_results, name='quiz_results'),
    
    # Categories
    path('categories/', views.category_list, name='category_list'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    
    # User progress
    path('progress/', views.progress_view, name='progress'),
    
    # Marking
    path('marking/', views.marking_list, name='marking_list'),
    path('marking/essay/<int:essay_answer_id>/', views.mark_essay, name='mark_essay'),
]