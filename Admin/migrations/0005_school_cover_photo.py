# Generated by Django 5.1.2 on 2024-10-29 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0004_alter_student_roll_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='cover_photo',
            field=models.ImageField(blank=True, null=True, upload_to='cover_photos/'),
        ),
    ]
