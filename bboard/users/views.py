from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, get_user_model

from .forms import RegistrationForm

User = get_user_model()
def registerView(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            user.first_name = form.cleaned_data['full_name']
            user.save()

            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('main:index')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'users/profile.html')