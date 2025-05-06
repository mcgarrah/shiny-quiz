def theme_context_processor(request):
    """
    Context processor to add theme information to all templates
    """
    dark_mode = False
    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        dark_mode = request.user.profile.dark_mode
    
    return {
        'dark_mode': dark_mode,
    }