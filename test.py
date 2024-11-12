from django.contrib.auth.models import AbstractUser
from django.db import models


#UserManagement
class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
        ('student', 'Student'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    school = models.ForeignKey('School', on_delete=models.CASCADE, null=True, blank=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    bio = models.TextField(blank=True)
    contact_number = models.CharField(max_length=15, blank=True)




#School&Classes
class School(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    contact_email = models.EmailField()
    unique_code = models.CharField(max_length=10, unique=True)  # For school registration
    qr_code = models.ImageField(upload_to='qrcodes/', null=True, blank=True)

class Class(models.Model):
    name = models.CharField(max_length=100)
    grade = models.IntegerField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    students = models.ManyToManyField(User, related_name='classes', limit_choices_to={'role': 'student'})




#Newsfeed
class Post(models.Model):
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    video = models.FileField(upload_to='posts/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role__in': ['admin', 'teacher']})
    target_grade = models.IntegerField(null=True, blank=True)  # Specific grades or school-wide
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class PostView(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)




#Messaging System
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    file = models.FileField(upload_to='messages/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

class ScheduledMessage(models.Model):
    message = models.OneToOneField(Message, on_delete=models.CASCADE)
    scheduled_time = models.DateTimeField()




#Events & Announcements
class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role__in': ['admin', 'teacher']})
    attendees = models.ManyToManyField(User, related_name='events')
    reminder_sent = models.BooleanField(default=False)

class Announcement(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role__in': ['admin', 'teacher']})
    created_at = models.DateTimeField(auto_now_add=True)
    target_group = models.CharField(max_length=50)  # Can be 'school-wide', 'grade-specific', etc.



#Dynamic Reward Category
class RewardCategory(models.Model):
    name = models.CharField(max_length=100)  # e.g., "Respectful", "Attentive"
    description = models.TextField(null=True, blank=True)  # Description of the category
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'admin'})
    created_at = models.DateTimeField(auto_now_add=True)




#Classroom Management (Points System)

# For individual points
class Point(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    category = models.ForeignKey(RewardCategory, on_delete=models.CASCADE)  # Dynamic category
    points = models.IntegerField(default=0)
    date_awarded = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(null=True, blank=True)

# For group points
class Group(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User, related_name='groups', limit_choices_to={'role': 'student'})
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})

class GroupPoint(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    category = models.ForeignKey(RewardCategory, on_delete=models.CASCADE)  # Dynamic category
    points = models.IntegerField(default=0)
    awarded_by = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    date_awarded = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(null=True, blank=True)



#Reports & Analytics
# For individual student behavior reports
class Report(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    date_from = models.DateField()
    date_to = models.DateField()
    total_points = models.IntegerField()
    behaviors_tracked = models.ManyToManyField(RewardCategory)

# For group behavior reports
class GroupReport(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_from = models.DateField()
    date_to = models.DateField()
    total_points = models.IntegerField()





# Notifications
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)



