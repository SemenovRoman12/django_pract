from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import DesignRequestForm
from .models import DesignRequest

def index(request):
    return render(request, 'main/index.html')

@login_required
def create_request(request):
    if request.method == 'POST':
        form = DesignRequestForm(request.POST, request.FILES)
        if form.is_valid():
            design_request = form.save(commit=False)
            design_request.user = request.user
            design_request.save()
            messages.success(request, 'Заявка успешно создана!')
            return redirect('users:profile')
    else:
        form = DesignRequestForm()
    return render(request, 'main/create_request.html', {'form': form})

@login_required
def delete_request(request, pk):
    design_request = get_object_or_404(DesignRequest, pk=pk, user=request.user)
    if design_request.status == 'new':
        design_request.delete()
        messages.success(request, 'Заявка успешно удалена!')
    else:
        messages.error(request, 'Нельзя удалить заявку, которая уже принята в работу или завершена.')
    return redirect('users:profile')
