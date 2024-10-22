from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    full_name = models.CharField(max_length=100, blank=False, verbose_name="ФИО")

    def __str__(self):
        return self.username

    class Meta(AbstractUser.Meta):
        verbose_name='Пользователь'
        verbose_name_plural='Пользователи'