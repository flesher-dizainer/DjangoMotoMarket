from django.db import models
from django.db.models import Avg
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self) -> str:
        return reverse('category_detail', kwargs={'pk': self.pk})


class Manufacturer(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

    def get_absolute_url(self) -> str:
        return reverse('manufacturer_detail', kwargs={'pk': self.pk})


class Model(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, verbose_name='Производитель')
    name = models.CharField(max_length=100, verbose_name='Название')

    def __str__(self):
        return f"{self.manufacturer.name} {self.name}"

    class Meta:
        ordering = ['name']
        verbose_name = 'Модель'
        verbose_name_plural = 'Модели'

    def get_absolute_url(self) -> str:
        return reverse('model_detail', kwargs={'pk': self.pk})


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.CASCADE,
        related_name='products'

    )
    model = models.ForeignKey(Model, verbose_name='Модель', on_delete=models.CASCADE, related_name='products')
    year = models.PositiveIntegerField(
        verbose_name='Год выпуска',
        validators=[MinValueValidator(1900), MaxValueValidator(datetime.now().year)]
    )
    engine_capacity = models.PositiveIntegerField(
        verbose_name='Объем двигателя',
        validators=[MinValueValidator(1), MaxValueValidator(5000)],
        help_text='см³'
    )
    price = models.DecimalField(
        verbose_name='Цена',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(10_000_000)]
    )
    color = models.CharField(max_length=50, verbose_name='Цвет')
    front_wheel_size = models.PositiveIntegerField(
        verbose_name='Переднее колесо',
        default=21,
        help_text='дюймы'
    )
    rear_wheel_size = models.PositiveIntegerField(
        verbose_name='Заднее колесо',
        default=18,
        help_text='дюймы'
    )
    frame_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Номер рамы'
    )
    description = models.TextField(blank=True, verbose_name='Описание')
    quantity = models.PositiveIntegerField(default=0, verbose_name='На складе')
    reserved = models.PositiveIntegerField(default=0, verbose_name='Резерв')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.model} ({self.year}) - {self.color}"

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['price']),
            models.Index(fields=['category', 'price']),
        ]
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    @property
    def available_quantity(self) -> int:
        return self.quantity - self.reserved

    def get_absolute_url(self) -> str:
        return reverse('products:product_detail', kwargs={'pk': self.pk})

    def get_rating(self) -> float:
        rating = self.reviews.filter(is_approved=True).aggregate(Avg('rating'))
        return round(rating['rating__avg'], 1) if rating['rating__avg'] else 0


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='Товар')
    image = models.ImageField(upload_to='products/%Y/%m/')

    def __str__(self):
        return f"Изображение {self.product}"

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class ProductReview(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(6)]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    author = models.CharField(max_length=100, verbose_name='Автор')
    text = models.TextField(help_text='Введите отзыв', verbose_name='Отзыв')
    rating = models.IntegerField(choices=RATING_CHOICES, help_text='Выберите рейтинг')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Отзыв {self.author} ({self.rating}/5)"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
