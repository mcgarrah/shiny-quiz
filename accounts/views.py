from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.models import UserProfile

@login_required
def profile(request):
    """User profile view"""
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Update profile
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.save()
        
        user_profile.bio = request.POST.get('bio', user_profile.bio)
        user_profile.dark_mode = 'dark_mode' in request.POST
        
        # Handle profile picture upload
        if 'profile_picture' in request.FILES:
            user_profile.profile_picture = request.FILES['profile_picture']
        
        user_profile.save()
        messages.success(request, 'Your profile has been updated.')
        return redirect('accounts:profile')
    
    return render(request, 'accounts/profile.html', {
        'profile': user_profile
    })