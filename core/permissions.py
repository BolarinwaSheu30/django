from django.core.exceptions import PermissionDenied
from functools import wraps
from .models import Course, Assignment, Enrollment

def teacher_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.profile.user_type != 'teacher':
            raise PermissionDenied("Only teachers can perform this action.")
        return view_func(request, *args, **kwargs)
    return wrapper

def student_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.profile.user_type != 'student':
            raise PermissionDenied("Only students can perform this action.")
        return view_func(request, *args, **kwargs)
    return wrapper

def course_owner_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        course = Course.objects.get(pk=kwargs.get('pk') or kwargs.get('course_pk'))
        if course.teacher != request.user:
            raise PermissionDenied("You are not the teacher of this course.")
        return view_func(request, *args, **kwargs)
    return wrapper

def enrolled_student_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        course_id = kwargs.get('pk') or kwargs.get('course_pk')
        course = Course.objects.get(pk=course_id)
        if not Enrollment.objects.filter(student=request.user, course=course).exists():
            raise PermissionDenied("You must be enrolled in this course to access it.")
        return view_func(request, *args, **kwargs)
    return wrapper

def assignment_owner_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        assignment = Assignment.objects.get(pk=kwargs.get('assignment_pk') or kwargs.get('pk'))
        if assignment.course.teacher != request.user:
            raise PermissionDenied("You are not the owner of this assignment.")
        return view_func(request, *args, **kwargs)
    return wrapper
