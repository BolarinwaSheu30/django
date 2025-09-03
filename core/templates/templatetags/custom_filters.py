from django import template
from core.models import Enrollment

register = template.Library()

@register.filter
def in_course(user, course):
    return Enrollment.objects.filter(student=user, course=course).exists()