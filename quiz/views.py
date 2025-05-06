from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse
from .models import (
    Category, Quiz, Question, Answer, 
    Sitting, Progress, EssayQuestion, EssayAnswer
)

def quiz_list(request):
    """View to list all published quizzes"""
    quizzes = Quiz.objects.filter(draft=False).order_by('-created_at')
    
    # Filter by category if provided
    category_id = request.GET.get('category')
    if category_id:
        quizzes = quizzes.filter(category_id=category_id)
    
    # Search functionality
    search_query = request.GET.get('q')
    if search_query:
        quizzes = quizzes.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(quizzes, 12)  # Show 12 quizzes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all categories for filter dropdown
    categories = Category.objects.all()
    
    return render(request, 'quiz/quiz_list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': category_id,
        'search_query': search_query
    })

def category_list(request):
    """View to list all categories"""
    categories = Category.objects.all()
    
    # Get user progress for each category if user is authenticated
    if request.user.is_authenticated:
        for category in categories:
            category.progress = category.get_progress(request.user)
    
    return render(request, 'quiz/category_list.html', {
        'categories': categories
    })

def category_detail(request, category_id):
    """View to show category details and quizzes"""
    category = get_object_or_404(Category, id=category_id)
    quizzes = Quiz.objects.filter(category=category, draft=False)
    
    # Get user progress for each quiz if user is authenticated
    if request.user.is_authenticated:
        for quiz in quizzes:
            progress = Progress.objects.filter(user=request.user, quiz=quiz).first()
            if progress:
                quiz.user_progress = progress.get_percent_correct()
                quiz.user_completed = True
            else:
                quiz.user_progress = 0
                quiz.user_completed = False
    
    return render(request, 'quiz/category_detail.html', {
        'category': category,
        'quizzes': quizzes
    })

def quiz_detail(request, slug):
    """View to show quiz details"""
    quiz = get_object_or_404(Quiz, slug=slug, draft=False)
    
    # Check if user has already completed this quiz
    user_sitting = None
    if request.user.is_authenticated:
        user_sitting = Sitting.objects.filter(
            user=request.user,
            quiz=quiz,
            complete=True
        ).first()
    
    return render(request, 'quiz/quiz_detail.html', {
        'quiz': quiz,
        'user_sitting': user_sitting
    })

@login_required
def take_quiz(request, slug):
    """View to take a quiz"""
    quiz = get_object_or_404(Quiz, slug=slug, draft=False)
    
    # Check if user has already completed this quiz and it's single attempt
    if quiz.single_attempt:
        sitting = Sitting.objects.filter(
            user=request.user,
            quiz=quiz,
            complete=True
        ).first()
        
        if sitting:
            messages.info(request, "You have already completed this quiz.")
            return redirect('quiz:quiz_results', sitting_id=sitting.id)
    
    # Check for an incomplete sitting
    sitting = Sitting.objects.filter(
        user=request.user,
        quiz=quiz,
        complete=False
    ).first()
    
    # Create a new sitting if none exists
    if not sitting:
        # Get questions based on quiz settings
        questions = quiz.get_questions()
        question_ids = [q.id for q in questions]
        
        # Create the sitting
        sitting = Sitting.objects.create(
            user=request.user,
            quiz=quiz,
            question_list=question_ids,
            question_order=question_ids
        )
    
    # Get the current question
    question_ids = sitting.question_list
    answered_ids = list(map(int, sitting.user_answers.keys())) if sitting.user_answers else []
    
    # Find the first unanswered question
    current_question = None
    for q_id in question_ids:
        if q_id not in answered_ids:
            current_question = Question.objects.get(id=q_id)
            break
    
    # If all questions are answered, complete the quiz
    if not current_question:
        return complete_quiz(request, sitting)
    
    # Process answer submission
    if request.method == 'POST':
        # Get the submitted answer
        answer_id = request.POST.get(f'question_{current_question.id}')
        essay_answer = request.POST.get(f'essay_{current_question.id}')
        
        if current_question.question_type == 'essay':
            # Save essay answer
            EssayAnswer.objects.create(
                question=current_question,
                sitting=sitting,
                answer=essay_answer
            )
            sitting.add_user_answer(current_question)
        else:
            # Save multiple choice or true/false answer
            if answer_id:
                answer = get_object_or_404(Answer, id=answer_id)
                sitting.add_user_answer(current_question, answer)
            else:
                messages.error(request, "Please select an answer.")
                return render(request, 'quiz/take_quiz.html', {
                    'quiz': quiz,
                    'question': current_question,
                    'sitting': sitting
                })
        
        # Show answer explanation if exam_paper is True
        if quiz.exam_paper:
            return render(request, 'quiz/answer_feedback.html', {
                'quiz': quiz,
                'question': current_question,
                'answer': answer if current_question.question_type != 'essay' else None,
                'sitting': sitting
            })
        
        # Redirect to next question
        return redirect('quiz:take_quiz', slug=quiz.slug)
    
    # Check if time limit is exceeded
    if quiz.time_limit > 0:
        time_elapsed = timezone.now() - sitting.start_time
        time_limit_seconds = quiz.time_limit * 60
        
        if time_elapsed.total_seconds() > time_limit_seconds:
            return complete_quiz(request, sitting)
        
        # Calculate remaining time
        remaining_seconds = time_limit_seconds - time_elapsed.total_seconds()
        remaining_minutes = int(remaining_seconds // 60)
        remaining_seconds = int(remaining_seconds % 60)
    else:
        remaining_minutes = None
        remaining_seconds = None
    
    return render(request, 'quiz/take_quiz.html', {
        'quiz': quiz,
        'question': current_question,
        'sitting': sitting,
        'remaining_minutes': remaining_minutes,
        'remaining_seconds': remaining_seconds,
        'total_questions': len(question_ids),
        'answered_questions': len(answered_ids)
    })

def complete_quiz(request, sitting):
    """Complete the quiz and show results"""
    if not sitting.complete:
        sitting.mark_quiz_complete()
        
        # Update progress
        total_questions = sitting.get_total_questions()
        progress, created = Progress.objects.get_or_create(
            user=sitting.user,
            quiz=sitting.quiz
        )
        progress.update_score(
            sitting.current_score,
            total_questions,
            sitting.current_score
        )
    
    return redirect('quiz:quiz_results', sitting_id=sitting.id)

@login_required
def quiz_results(request, sitting_id):
    """View to show quiz results"""
    sitting = get_object_or_404(Sitting, id=sitting_id)
    
    # Check if user is authorized to view this sitting
    if sitting.user != request.user and not request.user.has_perm('quiz.view_sittings'):
        messages.error(request, "You are not authorized to view these results.")
        return redirect('quiz:quiz_list')
    
    quiz = sitting.quiz
    questions = sitting.get_questions()
    user_answers = sitting.get_user_answers()
    
    # Get essay answers
    essay_answers = EssayAnswer.objects.filter(sitting=sitting)
    
    # Calculate score
    score_percent = sitting.get_percent_correct()
    passed = score_percent >= quiz.pass_mark
    
    return render(request, 'quiz/quiz_results.html', {
        'quiz': quiz,
        'sitting': sitting,
        'questions': questions,
        'user_answers': user_answers,
        'essay_answers': essay_answers,
        'score_percent': score_percent,
        'passed': passed
    })

@login_required
def progress_view(request):
    """View to show user progress across all quizzes"""
    user_progress = Progress.objects.filter(user=request.user).order_by('-created_at')
    
    # Group by category
    categories = Category.objects.all()
    for category in categories:
        category.quizzes_taken = 0
        category.quizzes_passed = 0
        category.total_score = 0
        category.total_questions = 0
        
        for progress in user_progress:
            if progress.quiz.category == category:
                category.quizzes_taken += 1
                if progress.get_percent_correct() >= progress.quiz.pass_mark:
                    category.quizzes_passed += 1
                category.total_score += progress.correct_answers
                category.total_questions += progress.total_questions
        
        if category.total_questions > 0:
            category.success_rate = int(category.total_score / category.total_questions * 100)
        else:
            category.success_rate = 0
    
    return render(request, 'quiz/progress.html', {
        'user_progress': user_progress,
        'categories': categories
    })

@permission_required('quiz.view_sittings')
def marking_list(request):
    """View to list all completed quizzes for marking"""
    # Get all sittings with essay answers
    essay_sittings = Sitting.objects.filter(
        complete=True,
        essay_answers__isnull=False
    ).distinct()
    
    # Filter by quiz if provided
    quiz_id = request.GET.get('quiz')
    if quiz_id:
        essay_sittings = essay_sittings.filter(quiz_id=quiz_id)
    
    # Filter by user if provided
    user_id = request.GET.get('user')
    if user_id:
        essay_sittings = essay_sittings.filter(user_id=user_id)
    
    # Pagination
    paginator = Paginator(essay_sittings, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all quizzes and users for filter dropdowns
    quizzes = Quiz.objects.all()
    users = User.objects.filter(quiz_sittings__isnull=False).distinct()
    
    return render(request, 'quiz/marking_list.html', {
        'page_obj': page_obj,
        'quizzes': quizzes,
        'users': users,
        'selected_quiz': quiz_id,
        'selected_user': user_id
    })

@permission_required('quiz.view_sittings')
def mark_essay(request, essay_answer_id):
    """View to mark an essay answer"""
    essay_answer = get_object_or_404(EssayAnswer, id=essay_answer_id)
    
    if request.method == 'POST':
        is_correct = request.POST.get('is_correct') == 'true'
        comments = request.POST.get('comments', '')
        
        essay_answer.is_correct = is_correct
        essay_answer.comments = comments
        essay_answer.save()
        
        # Update sitting score if answer is correct
        if is_correct:
            sitting = essay_answer.sitting
            sitting.current_score += 1
            sitting.save()
            
            # Update progress
            progress = Progress.objects.get(user=sitting.user, quiz=sitting.quiz)
            progress.correct_answers += 1
            progress.save()
        
        messages.success(request, "Essay answer marked successfully.")
        return redirect('quiz:marking_list')
    
    return render(request, 'quiz/mark_essay.html', {
        'essay_answer': essay_answer
    })