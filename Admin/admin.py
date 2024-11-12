from django.contrib import admin
from .models import User, School, Profile, Student

# Register your models here.

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(School)
admin.site.register(Student)