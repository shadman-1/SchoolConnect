from django.shortcuts import render, redirect
from Admin.forms import CustomUserCreationForm
from django.contrib.auth import login as auth_login

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Log the user in after successful registration
            return redirect('school_list')  # Redirect to some page after registration
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})
