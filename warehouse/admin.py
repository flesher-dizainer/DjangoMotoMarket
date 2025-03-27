from django.contrib import admin
from .models import StockMovement
#
#
# @admin.register(Warehouse)
# class WarehouseAdmin(admin.ModelAdmin):
#     list_display = ('product', 'get_quantity', 'get_available_quantity')
#     search_fields = ('product__name',)
#     list_filter = ('product__category',)
#
#     def get_quantity(self, obj):
#         return obj.quantity
#
#     get_quantity.short_description = 'Количество на складе'
#
#     def get_available_quantity(self, obj):
#         return obj.available_quantity
#
#     get_available_quantity.short_description = 'Доступное количество'
#
#
@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('product', 'movement_type', 'quantity', 'status', 'created_at')
    list_filter = ('movement_type', 'status', 'created_at')
    search_fields = ('product__model__name', 'comment')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
