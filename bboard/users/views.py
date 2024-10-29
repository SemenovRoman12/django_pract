from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm
from .forms import RegistrationForm
from .models import DesignRequest
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import RegistrationForm
from .models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import RegistrationForm
from .models import User


User = get_user_model()



def registerView(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)  # Добавляем request.FILES
        if form.is_valid():
            user = User.objects.create_user(
                full_name=form.cleaned_data['full_name'],
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                avatar=form.cleaned_data.get('avatar')  # Сохраняем аватар
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
    user_requests = DesignRequest.objects.filter(user=request.user)
    return render(request, 'users/profile.html', {'user_requests': user_requests})

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'users/profile.html', {'form': form})
