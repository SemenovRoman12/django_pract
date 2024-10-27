from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import DesignRequestForm, UpdateStatusForm
from .models import DesignRequest, Category


def index(request):
    completed_requests = DesignRequest.objects.filter(status='completed').order_by('-created_at')[:4]
    return render(request, 'main/index.html', {'completed_requests': completed_requests})

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

@staff_member_required
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Category.objects.create(name=name)
            messages.success(request, 'Категория успешно добавлена.')
        else:
            messages.error(request, 'Название категории не может быть пустым.')
    return redirect('main:manage_categories')

@staff_member_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Категория успешно удалена.')
    return redirect('main:manage_categories')


@staff_member_required
def manage_categories(request):
    categories = Category.objects.all()
    return render(request, 'main/manage_categories.html', {'categories': categories})

@staff_member_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    DesignRequest.objects.filter(category=category).delete()
    category.delete()
    messages.success(request, 'Категория и связанные с ней заявки успешно удалены.')
    return redirect('main:manage_categories')


@login_required
def update_request_status(request, pk):
    design_request = get_object_or_404(DesignRequest, pk=pk, user=request.user)

    if design_request.status not in ['new']:
        messages.error(request, 'Смена статуса возможна только для заявок со статусом "Новая".')
        return redirect('users:profile')

    if request.method == 'POST':
        form = UpdateStatusForm(request.POST, request.FILES, instance=design_request)
        if form.is_valid():
            form.save()
            messages.success(request, 'Статус заявки успешно обновлен.')
            return redirect('users:profile')
    else:
        form = UpdateStatusForm(instance=design_request)

    return render(request, 'main/update_request_status.html', {'form': form, 'design_request': design_request})