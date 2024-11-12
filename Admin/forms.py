from django import forms
from .models import School
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name', 'address', 'contact_email', 'unique_code', 'qr_code']  # Include the fields you want in the form

        # Optional: Add custom widgets or labels if you need to customize form field appearance
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'unique_code': forms.TextInput(attrs={'class': 'form-control'}),
            'qr_code': forms.FileInput(attrs={'class': 'form-control'}),
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta: 
        model = User# or get_user_model() if using a custom user model
        fields = ['username', 'password1', 'password2']

    # Apply the Bootstrap form-control class to all fields
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


# class StudentForm(forms.ModelForm):
    #class Meta:
        #model = Student
        #fields = ['school','name', 'email', 'registration_number','roll_number']