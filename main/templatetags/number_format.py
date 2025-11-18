from django import template

register = template.Library()

def humanize_number(value):
    try:
        value = int(value)
    except (ValueError, TypeError):
        return value

    if value >= 1_000_000:
        return f"{value/1_000_000:.1f}M".rstrip('0').rstrip('.')
    elif value >= 1_000:
        return f"{value/1_000:.1f}K".rstrip('0').rstrip('.')
    else:
        return str(value)

register.filter('humanize_number', humanize_number)