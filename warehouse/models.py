"""
Модель склада. То есть движения товара.
Количество товара на складе вычисляется из суммы всех входящих движений.
Напрямую изменять количество товара на складе нельзя, только через движения товара.
"""
from django.core.validators import MinValueValidator
from products.models import Product  # Импортируем модель Product из приложения products
from django.db import models
from django.db.models import Sum

# Модель движения товара.
class StockMovement(models.Model):
    MOVEMENT_TYPES = [
        ('incoming', 'Поступление'),
        ('outgoing', 'Списание в брак'),
        ('sale', 'Продажа'),
        ('return', 'Возврат'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Ожидание'),
        ('completed', 'Выполнен'),
        ('reserved', 'Зарезервирован'),
        ('canceled', 'Отменен'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар',
                                related_name='stock_movements')
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES, verbose_name='Тип операции')
    quantity = models.IntegerField(verbose_name='Количество', validators=[MinValueValidator(1)], default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата операции')
    comment = models.TextField(blank=True, verbose_name='Комментарий')

    def __str__(self):
        return f"{self.get_movement_type_display()} - {self.product.model.name} ({self.product.quantity} шт.)"

    class Meta:
        verbose_name = 'Движение товара'
        verbose_name_plural = 'Движения товаров'
        ordering = ['-created_at']
