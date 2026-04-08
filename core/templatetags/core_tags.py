from django import template
from core.models import Profile

register = template.Library()

@register.filter
def get_recent_students(profile):
    return Profile.objects.exclude(user=profile.user).order_by('?')[:5]
