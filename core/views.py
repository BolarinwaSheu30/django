from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import RegistrationForm
from .models import Assignment, Profile, Course, Enrollment, Submission
from .permissions import (
    teacher_required, student_required,
    course_owner_required, enrolled_student_required,
    assignment_owner_required
)


def home(request):
    return render(request, 'home.html', {'user': request.user})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def course_list(request):
    if request.user.profile.user_type == 'teacher':
        courses = Course.objects.filter(teacher=request.user)
    else:
        courses = Course.objects.all()

    enrolled_courses = []
    if request.user.profile.user_type == 'student':
        enrolled_courses = list(
            Enrollment.objects.filter(student=request.user)
            .values_list('course_id', flat=True)
        )

    return render(request, 'courses/list.html', {
        'courses': courses,
        'enrolled_courses': enrolled_courses
    })


@login_required
@teacher_required
def course_create(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        Course.objects.create(title=title, description=description, teacher=request.user)
        return redirect('course_list')
    return render(request, 'courses/create.html')


@login_required
@course_owner_required
def course_update(request, pk):
    course = Course.objects.get(pk=pk)
    if request.method == 'POST':
        course.title = request.POST['title']
        course.description = request.POST['description']
        course.save()
        return redirect('course_list')
    return render(request, 'courses/update.html', {'course': course})


@login_required
@course_owner_required
def course_delete(request, pk):
    course = Course.objects.get(pk=pk)
    course.delete()
    return redirect('course_list')


@login_required
@student_required
def enroll(request, pk):
    course = Course.objects.get(pk=pk)
    Enrollment.objects.get_or_create(student=request.user, course=course)
    return redirect('course_list')


@login_required
def assignment_list(request, course_pk):
    course = Course.objects.get(pk=course_pk)

    if request.user.profile.user_type == 'teacher' and request.user != course.teacher:
        return HttpResponseForbidden()
    if request.user.profile.user_type == 'student' and not Enrollment.objects.filter(student=request.user, course=course).exists():
        return HttpResponseForbidden("Enroll first.")

    assignments = Assignment.objects.filter(course=course)

    submitted_assignments = []
    if request.user.profile.user_type == 'student':
        submitted_assignments = list(
            Submission.objects.filter(student=request.user, assignment__course=course)
            .values_list('assignment_id', flat=True)
        )

    return render(request, 'assignments/list.html', {
        'assignments': assignments,
        'course': course,
        'submitted_assignments': submitted_assignments
    })


@login_required
@course_owner_required
def assignment_create(request, course_pk):
    course = Course.objects.get(pk=course_pk)
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        Assignment.objects.create(title=title, description=description, course=course)
        return redirect('assignment_list', course_pk=course_pk)
    return render(request, 'assignments/create.html', {'course': course})


@login_required
@student_required
def submission_create(request, assignment_pk):
    assignment = Assignment.objects.get(pk=assignment_pk)

    if not Enrollment.objects.filter(student=request.user, course=assignment.course).exists():
        return HttpResponseForbidden()

    already_submitted = Submission.objects.filter(student=request.user, assignment=assignment).exists()
    if already_submitted:
        return HttpResponseForbidden("Already submitted.")

    if request.method == 'POST':
        response = request.POST['response']
        Submission.objects.create(student=request.user, assignment=assignment, response=response)
        return redirect('assignment_list', course_pk=assignment.course.pk)

    return render(request, 'submissions/create.html', {
        'assignment': assignment,
        'already_submitted': already_submitted
    })


@login_required
@assignment_owner_required
def submission_list(request, assignment_pk):
    assignment = Assignment.objects.get(pk=assignment_pk)
    submissions = Submission.objects.filter(assignment=assignment)
    return render(request, 'submissions/list.html', {'submissions': submissions, 'assignment': assignment})


@login_required
@assignment_owner_required
def submission_review(request, pk):
    submission = Submission.objects.get(pk=pk)
    submission.reviewed = True
    submission.save()
    return redirect('submission_list', assignment_pk=submission.assignment.pk)
