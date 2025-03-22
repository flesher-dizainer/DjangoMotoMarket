from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime

# Категории товаров
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'pk': self.pk})


# Модели товаров
class Model(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Модель'
        verbose_name_plural = 'Модели'

    def get_absolute_url(self):
        return reverse('model_detail', kwargs={'pk': self.pk})


# Модель товара мотоцикла
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория',
                                 related_name='products')
    model = models.ForeignKey(Model, on_delete=models.CASCADE, verbose_name='Модель',
                              related_name='products')
    name = models.CharField(max_length=100, verbose_name='Название')
    year = models.PositiveIntegerField(
        verbose_name='Год выпуска',
        validators=[MinValueValidator(1900), MaxValueValidator(datetime.now().year)]
    )
    engine_capacity = models.PositiveIntegerField(
        verbose_name='Объем двигателя',
        validators=[MinValueValidator(1), MaxValueValidator(5000)],
        help_text='Введите объем двигателя в кубических сантиметрах'
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Цена',
        validators=[MinValueValidator(0), MaxValueValidator(1000000)]
    )
    color = models.CharField(max_length=50, verbose_name='Цвет')
    # Размер переднего колеса
    front_wheel_size = models.PositiveIntegerField(
        verbose_name='Размер переднего колеса',
        validators=[MinValueValidator(10), MaxValueValidator(100)],
        help_text='Введите размер переднего колеса в дюймах',
        default=21
    )
    # Размер заднего колеса
    rear_wheel_size = models.PositiveIntegerField(
        verbose_name='Размер заднего колеса',
        validators=[MinValueValidator(10), MaxValueValidator(100)],
        help_text='Введите размер заднего колеса в дюймах',
        default=18
    )
    description = models.TextField(blank=True, verbose_name='Описание')
    image = models.ImageField(upload_to='products/%Y/%m/', verbose_name='Изображение', blank=True, null=True)
    is_available = models.BooleanField(default=True, verbose_name='В наличии')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    # SEO поля
    meta_title = models.CharField(max_length=150, blank=True, verbose_name='Meta Title')
    meta_description = models.TextField(blank=True, verbose_name='Meta Description')
    meta_keywords = models.CharField(max_length=200, blank=True, verbose_name='Meta Keywords')

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f"{self.name} ({self.year})"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['price']),
            models.Index(fields=['category', 'price']),  # Составной индекс
        ]