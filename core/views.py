from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from quiz.models import Quiz
from core.models import UserProfile

def home(request):
    """Home page view showing featured quizzes"""
    featured_quizzes = Quiz.objects.filter(draft=False).order_by('-created_at')[:6]
    return render(request, 'core/home.html', {
        'featured_quizzes': featured_quizzes,
    })

def about(request):
    """About page view"""
    return render(request, 'core/about.html')

def contact(request):
    """Contact page view"""
    return render(request, 'core/contact.html')

@login_required
def toggle_theme(request):
    """Toggle between light and dark theme"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            dark_mode = data.get('dark_mode', False)
            
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            user_profile.dark_mode = dark_mode
            user_profile.save()
            
            return JsonResponse({'success': True, 'dark_mode': dark_mode})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)