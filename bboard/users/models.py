from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    full_name = models.CharField(max_length=100, blank=False, verbose_name="ФИО")
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="Аватар")

    def str(self):
        return self.username

    class Meta(AbstractUser.Meta):
        verbose_name='Пользователь'
        verbose_name_plural='Пользователи'


class DesignRequest:
    pass
