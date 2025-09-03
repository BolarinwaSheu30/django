from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/create/', views.course_create, name='course_create'),
    path('courses/<int:pk>/update/', views.course_update, name='course_update'),
    path('courses/<int:pk>/delete/', views.course_delete, name='course_delete'),
    path('courses/<int:pk>/enroll/', views.enroll, name='enroll'),
    path('courses/<int:course_pk>/assignments/',views.assignment_list, name='assignment_list'),
    path('courses/<int:course_pk>/assignments/create/', views.assignment_create, name='assignment_create'),
    

    path('assignments/<int:assignment_pk>/submit/', views.submission_create, name='submission_create'),
    path('assignments/<int:assignment_pk>/submissions/', views.submission_list, name='submission_list'),
    path('submissions/<int:pk>/review/', views.submission_review, name='submission_review'),
]


from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import CourseViewSet, AssignmentViewSet, SubmissionViewSet, EnrollmentViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'assignments', AssignmentViewSet)
router.register(r'submissions', SubmissionViewSet)
router.register(r'enrollments', EnrollmentViewSet)

urlpatterns += [
    path('api/', include(router.urls)),   # 👈 API lives under /api/
]
