from django.contrib import admin
from .models import Assignment, Profile,Course, Enrollment

admin.site.register(Profile)
admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(Assignment)