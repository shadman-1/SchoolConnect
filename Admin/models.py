from django.contrib.auth.models import AbstractUser
from django.db import models


#UserManagement

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
        ('student', 'Student'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    school = models.ForeignKey('School', on_delete=models.CASCADE, null=True, blank=True)

    # Add related_name to avoid clashes
    groups = models.ManyToManyField(Group,
        related_name='custom_user_groups',  # Make this unique
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',  # Make this unique
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    bio = models.TextField(blank=True)
    contact_number = models.CharField(max_length=15, blank=True)

class School(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    contact_email = models.EmailField()
    unique_code = models.CharField(max_length=10, unique=True)  # For school registration
    qr_code = models.ImageField(upload_to='qrcodes/', null=True, blank=True)
    cover_photo = models.ImageField(upload_to='cover_photos/', blank=True, null=True) 

    def __str__(self) -> str:
        return (f"School Name : {self.name}, located at - {self.address}")
    
    
    #class Class(models.Model):
    #name = models.CharField(max_length=100)
    #grade = models.IntegerField()
    #teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    #students = models.ManyToManyField(User, related_name='classes', limit_choices_to={'role': 'student'})


class Student(models.Model):
    school = models.ForeignKey(School, related_name='students', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    registration_number = models.CharField(max_length=10)
    roll_number = models.IntegerField(null=True, blank=True)   

    def __str__(self):
        return (f"Name: {self.name}, school: studied at {self.school.name}")