"""
Модель пользователей. Пользователи могут быть админы, менеджеры, обычные пользователи.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.urls import reverse


def user_avatar_path(instance, filename):
    return f'user_avatars/user_{instance.id}/{filename}'


class CustomUser(AbstractUser):
    """Модель пользователя"""
    # Типы пользователей
    USER_TYPE_CHOICES = (
        ('admin', 'Администратор'),
        ('manager', 'Менеджер'),
        ('customer', 'Пользователь'),
    )
    # Тип пользователя
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='customer',
        verbose_name='Тип пользователя'
    )
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(unique=True, max_length=15, blank=True, null=True, verbose_name='Телефон')
    avatar = models.ImageField(
        upload_to=user_avatar_path,
        blank=True,
        null=True,
        verbose_name='Аватар'
    )
    bio = models.TextField(blank=True, null=True, verbose_name='О себе')
    date_of_birth = models.DateField(blank=True, null=True, verbose_name='Дата рождения')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def get_avatar_url(self):
        """Возвращает URL аватара или URL аватара по умолчанию"""
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        return f"{settings.STATIC_URL}img/default_avatar.png"

    def get_absolute_url(self):
        """Возвращает URL профиля пользователя"""
        return reverse('users:profile', kwargs={'username': self.username})
