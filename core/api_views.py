from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from .models import Course, Assignment, Submission, Enrollment
from .serializers import (
    CourseSerializer, AssignmentSerializer, SubmissionSerializer,
    EnrollmentSerializer, StudentSerializer
)



class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = [permissions.AllowAny]  # for testing; secure later

    def get_queryset(self):
        return User.objects.filter(profile__user_type='student').select_related('profile')


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.AllowAny]


class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.AllowAny]


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.AllowAny]
