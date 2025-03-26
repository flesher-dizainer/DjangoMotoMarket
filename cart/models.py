from django.core.validators import MinValueValidator
from django.db import models
from django.conf import settings
from products.models import Product
from users.models import CustomUser


class Cart(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        ordering = ['-created_at']

    def __str__(self):
        return f"Корзина пользователя {self.user.username}"

    @classmethod
    def get_or_create_cart(cls, request):
        if request.user.is_authenticated:
            cart, _ = cls.objects.get_or_create(user=request.user)
            return cart
        return None

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @classmethod
    def get_cart(cls, user):
        if user.is_authenticated:
            cart, _ = cls.objects.get_or_create(user=user)
            return cart
        return None


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Корзина'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар'
    )
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name='Количество'
    )
    added_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления'
    )

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'
        unique_together = ('cart', 'product')
        ordering = ['added_at']

    def __str__(self):
        return f"{self.quantity} x {self.product.model.name}"

    @property
    def total_price(self):
        return self.quantity * self.product.price
