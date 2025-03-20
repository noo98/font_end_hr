from django import template

register = template.Library()

@register.filter
def endswith(value, arg):
    """Check if string ends with a specific suffix"""
    if value and isinstance(value, str):
        return value.lower().endswith(arg.lower())
    return False