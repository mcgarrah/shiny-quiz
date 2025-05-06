from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Template filter to access dictionary items by key
    Usage: {{ dictionary|get_item:key }}
    """
    if dictionary is None:
        return None
    
    try:
        return dictionary.get(int(key))
    except (ValueError, AttributeError, TypeError):
        try:
            return dictionary.get(key)
        except (AttributeError, TypeError):
            try:
                return dictionary[key]
            except (KeyError, TypeError):
                return None

@register.filter
def count_marked_essays(essay_answers):
    """
    Count the number of essay answers that have been marked (is_correct is not None)
    Usage: {{ sitting.essay_answers.all|count_marked_essays }}
    """
    return essay_answers.exclude(is_correct=None).count()

@register.filter
def first_unmarked_essay(essay_answers):
    """
    Get the first unmarked essay answer (is_correct is None)
    Usage: {{ sitting.essay_answers.all|first_unmarked_essay }}
    """
    unmarked = essay_answers.filter(is_correct=None).first()
    return unmarked