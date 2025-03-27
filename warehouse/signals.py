from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.db import transaction

from warehouse.models import StockMovement


@receiver(post_save, sender=StockMovement)
def update_product_quantity_on_movement(sender, instance, created, **kwargs):
    """
    Обновляет количество товара при создании/изменении движения товара.
    """
    with transaction.atomic():
        product = instance.product
        if instance.status == 'completed':
            # Определяем, увеличивать или уменьшать количество
            if instance.movement_type in ['incoming', 'return']:
                product.quantity += instance.quantity
            elif instance.movement_type in ['outgoing', 'sale']:
                product.quantity -= instance.quantity

            # Гарантируем, что количество не станет отрицательным
            product.quantity = max(product.quantity, 0)
            product.save(update_fields=['quantity'])


@receiver(post_delete, sender=StockMovement)
def revert_product_quantity_on_delete(sender, instance, **kwargs):
    """
    Возвращает количество товара при удалении движения.
    """
    with transaction.atomic():
        product = instance.product
        if instance.status == 'completed':
            if instance.movement_type in ['incoming', 'return']:
                product.quantity -= instance.quantity
            elif instance.movement_type in ['outgoing', 'sale']:
                product.quantity += instance.quantity

            product.quantity = max(product.quantity, 0)
            product.save(update_fields=['quantity'])