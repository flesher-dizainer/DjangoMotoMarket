from django.contrib import admin
from .models import Category, Model, Product

# Регистрация модели Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at')
    fields = ('name', 'description')  # Поля для редактирования


# Регистрация модели Model
@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at')
    fields = ('name',)  # Поля для редактирования


# Регистрация модели Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'model', 'year', 'front_wheel_size', 'rear_wheel_size', 'price', 'is_available', 'created_at', 'updated_at')
    search_fields = ('name', 'category__name', 'model__name')
    list_filter = ('category', 'model', 'year', 'is_available', 'created_at', 'front_wheel_size', 'rear_wheel_size')
    fieldsets = (
        (None, {
            'fields': ('category', 'model', 'name', 'year', 'front_wheel_size', 'rear_wheel_size', 'engine_capacity', 'price', 'color')
        }),
        ('Описание и изображение', {
            'fields': ('description', 'image')
        }),
        ('Наличие и SEO', {
            'fields': ('is_available', 'meta_title', 'meta_description', 'meta_keywords')
        }),
    )