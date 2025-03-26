from django.db.models.signals import post_save
from django.dispatch import receiver

from cart.models import Cart
from users.models import CustomUser


@receiver(post_save, sender=CustomUser)
def create_user_cart(sender, instance, created, **kwargs):
    """Создает корзину для нового пользователя при регистрации"""
    if created:
        Cart.objects.create(user=instance)
