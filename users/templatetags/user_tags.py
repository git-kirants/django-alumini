from django import template

register = template.Library()

@register.filter
def get_initials(user):
    """Get user's initials from first_name and last_name or username"""
    if user.first_name and user.last_name:
        return f"{user.first_name[0]}{user.last_name[0]}".upper()
    return user.username[0].upper() 