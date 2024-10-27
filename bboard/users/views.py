from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, get_user_model

from .forms import RegistrationForm
from main.models import DesignRequest

User = get_user_model()
def registerView(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                full_name=form.cleaned_data['full_name'],
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            user.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('users:profile')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    status_filter = request.GET.get('status', 'all')
    if status_filter == 'all':
        user_requests = DesignRequest.objects.filter(user=request.user)
    else:
        user_requests = DesignRequest.objects.filter(user=request.user, status=status_filter)

    return render(request, 'users/profile.html', {
        'user_requests': user_requests,
        'status_filter': status_filter,
    })