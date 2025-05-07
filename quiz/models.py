from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field
from django.db.models import JSONField

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('quiz:category_detail', args=[self.id])
    
    @property
    def get_quizzes(self):
        return Quiz.objects.filter(category=self, draft=False)
    
    def get_progress(self, user):
        """
        Returns user progress for a specific category
        """
        if not user.is_authenticated:
            return None
        
        total = 0
        correct = 0
        
        for quiz in self.get_quizzes:
            progress = Progress.objects.filter(user=user, quiz=quiz).first()
            if progress:
                total += progress.total_questions
                correct += progress.correct_answers
        
        if total > 0:
            return int(correct / total * 100)
        return 0

class Quiz(models.Model):
    title = models.CharField(max_length=255, db_index=True)  # Index for searching by title
    slug = models.SlugField(max_length=255, unique=True, blank=True, db_index=True)  # Already indexed by unique=True
    description = CKEditor5Field(blank=True, config_name='extends')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='quizzes', db_index=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_quizzes', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)  # Index for sorting by creation date
    updated_at = models.DateTimeField(auto_now=True)
    
    # Quiz settings
    random_order = models.BooleanField(default=False, help_text="Display questions in random order")
    max_questions = models.IntegerField(default=0, help_text="0 = All questions")
    answers_at_end = models.BooleanField(default=False, help_text="Show all answers at the end")
    exam_paper = models.BooleanField(default=False, help_text="If yes, answers show after each question")
    single_attempt = models.BooleanField(default=False, help_text="If yes, only one attempt is allowed")
    pass_mark = models.FloatField(default=50, help_text="Percentage required to pass")
    success_text = CKEditor5Field(blank=True, config_name='default', help_text="Displayed if user passes")
    fail_text = CKEditor5Field(blank=True, config_name='default', help_text="Displayed if user fails")
    draft = models.BooleanField(default=False, db_index=True, help_text="If yes, quiz is not displayed in the quiz list")  # Index for filtering published quizzes
    time_limit = models.IntegerField(default=0, help_text="Time limit in minutes (0 = no limit)")
    
    class Meta:
        verbose_name_plural = "Quizzes"
        ordering = ['-created_at']
        permissions = [
            ("view_sittings", "Can view quiz results from users"),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('quiz:quiz_detail', args=[self.slug])
    
    @property
    def question_count(self):
        return self.questions.count()
    
    def get_questions(self):
        """
        Returns questions based on quiz settings
        """
        questions = self.questions.all()
        if self.random_order:
            questions = questions.order_by('?')
        if self.max_questions > 0:
            questions = questions[:self.max_questions]
        return questions

class Question(models.Model):
    """
    Base class for all question types
    """
    QUESTION_TYPE_CHOICES = (
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('essay', 'Essay'),
    )
    
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions', db_index=True)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES, default='multiple_choice', db_index=True)  # Index for filtering by question type
    text = CKEditor5Field(config_name='extends')
    explanation = CKEditor5Field(blank=True, config_name='default', help_text="Explanation shown after question is answered")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return self.text[:50]
    
    @property
    def correct_answer(self):
        """
        Returns the correct answer for this question
        """
        if self.question_type == 'multiple_choice':
            return self.answers.filter(is_correct=True).first()
        elif self.question_type == 'true_false':
            return self.answers.filter(is_correct=True).first()
        return None
    
    @property
    def get_answers(self):
        """
        Returns answers based on question type
        """
        if self.question_type in ['multiple_choice', 'true_false']:
            return self.answers.all()
        return None
    
    def check_if_correct(self, selected_answer):
        """
        Checks if the selected answer is correct
        """
        if self.question_type == 'essay':
            return None  # Essay questions need manual grading
        
        if selected_answer:
            return selected_answer.is_correct
        return False

class Answer(models.Model):
    """
    Answer model for multiple choice and true/false questions
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', db_index=True)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False, db_index=True)  # Index for filtering correct answers
    
    def __str__(self):
        return f"{self.text} ({'Correct' if self.is_correct else 'Incorrect'})"

class Sitting(models.Model):
    """
    Records a user's progress through a quiz
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_sittings', db_index=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='sittings', db_index=True)
    question_order = JSONField(default=list)
    question_list = JSONField(default=list)
    incorrect_questions = JSONField(default=list)
    current_score = models.IntegerField(default=0)
    complete = models.BooleanField(default=False, db_index=True)  # Index for filtering complete/incomplete sittings
    user_answers = JSONField(default=dict)
    start_time = models.DateTimeField(auto_now_add=True, db_index=True)  # Index for time-based queries
    end_time = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        permissions = [
            ("view_sittings", "Can view quiz results from users"),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.quiz.title}"
    
    def get_percent_correct(self):
        """
        Returns the percentage of correct answers
        """
        if self.current_score > 0:
            return int(self.current_score / self.get_total_questions() * 100)
        return 0
    
    def mark_quiz_complete(self):
        """
        Marks the quiz as complete and sets the end time
        """
        self.complete = True
        self.end_time = timezone.now()
        self.save()
    
    def add_user_answer(self, question, answer=None):
        """
        Adds a user answer to the sitting
        """
        try:
            # Initialize user_answers if it's None
            if self.user_answers is None:
                self.user_answers = {}
                
            # Store the answer in the user_answers dictionary
            question_id = str(question.id)
            if answer:
                self.user_answers[question_id] = answer.id
            else:
                self.user_answers[question_id] = None
            
            # Initialize incorrect_questions if it's None
            if self.incorrect_questions is None:
                self.incorrect_questions = []
                
            # Update score and incorrect questions list
            if question.check_if_correct(answer) is True:
                self.current_score += 1
            else:
                if question.id not in self.incorrect_questions:
                    self.incorrect_questions.append(question.id)
            
            self.save()
        except (AttributeError, TypeError) as e:
            # Log the error (in a real application, use proper logging)
            print(f"Error adding user answer: {e}")
            # Initialize fields if they're None
            if self.user_answers is None:
                self.user_answers = {}
            if self.incorrect_questions is None:
                self.incorrect_questions = []
            self.save()
    
    def get_total_questions(self):
        """
        Returns the total number of questions in this sitting
        """
        try:
            # Ensure question_list is a valid list
            if self.question_list is None:
                return 0
            return len(self.question_list)
        except (TypeError, ValueError):
            # Handle case where question_list is not a valid list
            return 0
    
    def get_questions(self):
        """
        Returns the list of questions for this sitting
        """
        try:
            # Ensure question_list is a valid list of IDs
            if not self.question_list:
                return Question.objects.none()
                
            # Filter questions by ID
            return Question.objects.filter(id__in=self.question_list)
        except (TypeError, ValueError):
            # Handle case where question_list is not a valid list
            return Question.objects.none()
    
    def get_incorrect_questions(self):
        """
        Returns the list of incorrect questions
        """
        try:
            # Ensure incorrect_questions is a valid list of IDs
            if not self.incorrect_questions:
                return Question.objects.none()
                
            # Filter questions by ID
            return Question.objects.filter(id__in=self.incorrect_questions)
        except (TypeError, ValueError):
            # Handle case where incorrect_questions is not a valid list
            return Question.objects.none()
    
    def get_user_answers(self):
        """
        Returns a dictionary of user answers
        """
        if not self.user_answers:
            return {}
            
        try:
            # Convert string keys to integers and ensure values are properly typed
            return {
                int(k): (int(v) if v is not None else None) 
                for k, v in self.user_answers.items()
            }
        except (ValueError, TypeError, AttributeError):
            # Handle any conversion errors
            return {}
    
    def is_passed(self):
        """
        Returns True if the user has passed the quiz
        """
        return self.get_percent_correct() >= self.quiz.pass_mark

class Progress(models.Model):
    """
    Tracks user progress across quizzes and categories
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_progress', db_index=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='progress', db_index=True)
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)  # Index for time-based queries
    
    class Meta:
        verbose_name_plural = "Progress Records"
        unique_together = ['user', 'quiz']
        indexes = [
            models.Index(fields=['user', 'quiz']),  # Composite index for the common query pattern
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.quiz.title}"
    
    def update_score(self, score, total, correct):
        """
        Updates the user's score for this quiz
        """
        self.score = score
        self.total_questions = total
        self.correct_answers = correct
        self.save()
    
    def get_percent_correct(self):
        """
        Returns the percentage of correct answers
        """
        if self.total_questions > 0:
            return int(self.correct_answers / self.total_questions * 100)
        return 0

class EssayQuestion(models.Model):
    """
    Model for essay questions that need manual grading
    """
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name='essay_question')
    answer = models.TextField(blank=True, help_text="Model answer for this essay question")
    
    def __str__(self):
        return self.question.text[:50]

class EssayAnswer(models.Model):
    """
    Model for storing user's essay answers
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='essay_answers', db_index=True)
    sitting = models.ForeignKey(Sitting, on_delete=models.CASCADE, related_name='essay_answers', db_index=True)
    answer = models.TextField(blank=True)
    is_correct = models.BooleanField(null=True, blank=True, db_index=True)  # Index for filtering marked/unmarked essays
    comments = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.sitting.user.username} - {self.question.text[:30]}"