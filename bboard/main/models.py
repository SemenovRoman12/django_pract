from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import models
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect

user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='requests')

from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Название категории")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class DesignRequest(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'Принято в работу'),
        ('completed', 'Выполнено')
    ]

    title = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    image = models.ImageField(upload_to='requests_img/', verbose_name="Фото помещения", blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='requests')
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True)
    design_image = models.ImageField(upload_to='design_images/', verbose_name="Изображение дизайна", blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'


@login_required
def update_status(request, pk, status):
    design_request = get_object_or_404(DesignRequest, pk=pk, user=request.user)

    if design_request.status == 'new':
        if status == 'in_progress':
            design_request.status = 'in_progress'
            design_request.save()
            messages.success(request, 'Заявка успешно принята в работу.')
        elif status == 'completed':
            design_request.status = 'completed'
            design_request.save()
            messages.success(request, 'Заявка успешно завершена.')
        else:
            messages.error(request, 'Недопустимый статус.')
    else:
        messages.error(request, 'Статус заявки уже был изменен, и ее нельзя обновить.')

    return redirect('users:profile')