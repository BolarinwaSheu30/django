from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core.views import register, home
from rest_framework import routers
from core import api_views  


router = routers.DefaultRouter()
router.register(r'students', api_views.StudentViewSet, basename='student')
router.register(r'courses', api_views.CourseViewSet, basename='course')
router.register(r'assignments', api_views.AssignmentViewSet, basename='assignment')
router.register(r'submissions', api_views.SubmissionViewSet, basename='submission')
router.register(r'enrollments', api_views.EnrollmentViewSet, basename='enrollment')

urlpatterns = [
    
    path('admin/', admin.site.urls),

    # Django auth views
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Core app (HTML views)
    path('', home, name='home'),
    path('', include('core.urls')),

    # API routes (for Postman)
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')), 
]
