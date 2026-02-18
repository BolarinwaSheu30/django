from functools import wraps
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from .models import Course, Enrollment, Assignment

def course_owner_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        course_pk = kwargs.get("pk") or kwargs.get("course_pk")
        course = Course.objects.get(pk=course_pk)
        if course.teacher != request.user:
            raise PermissionDenied("You are not the teacher of this course.")
        return view_func(request, *args, **kwargs)
    return login_required(wrapper)


def enrolled_student_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        course_pk = kwargs.get("pk") or kwargs.get("course_pk")
        course = Course.objects.get(pk=course_pk)
        if not Enrollment.objects.filter(student=request.user, course=course).exists():
            raise PermissionDenied("You are not enrolled in this course.")
        return view_func(request, *args, **kwargs)
    return login_required(wrapper)


def assignment_owner_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        assignment_pk = kwargs.get("assignment_pk")
        assignment = Assignment.objects.get(pk=assignment_pk)
        if assignment.course.teacher != request.user:
            raise PermissionDenied("You are not the teacher of this course.")
        return view_func(request, *args, **kwargs)
    return login_required(wrapper)
