from django import template

register = template.Library()

@register.filter
def get_initials(user):
    """Get user's initials from full name or username."""
    if user.get_full_name():
        names = user.get_full_name().split()
        initials = ''.join(name[0].upper() for name in names if name)
    else:
        initials = user.username[0:2].upper()
    return initials 