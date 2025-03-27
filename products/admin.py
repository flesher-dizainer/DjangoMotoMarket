from django.contrib import admin
from .models import Category, Manufacturer, Model, Product, ProductImage, ProductReview


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer')
    list_filter = ('manufacturer',)
    search_fields = ('name', 'manufacturer__name')


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            from django.utils.html import format_html
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "-"

    image_preview.short_description = "Превью"


class ProductReviewInline(admin.TabularInline):
    model = ProductReview
    extra = 0
    fields = ('author', 'rating', 'text', 'is_approved')
    readonly_fields = ('author', 'rating', 'text', 'created_at')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'model',
        'year',
        'color',
        'price',
        'available_quantity',
        'get_rating'
    )
    list_filter = (
        'category',
        'model__manufacturer',
        'model',
        'year',
        'color'
    )
    search_fields = (
        'model__name',
        'model__manufacturer__name',
        'frame_number',
        'description'
    )
    readonly_fields = ('created_at', 'updated_at', 'available_quantity')
    fieldsets = (
        (None, {
            'fields': (
                'category',
                'model',
                'year',
                'engine_capacity',
                'price',
                'color'
            )
        }),
        ('Колёса', {
            'fields': (
                'front_wheel_size',
                'rear_wheel_size'
            ),
            'classes': ('collapse',)
        }),
        ('Инвентаризация', {
            'fields': (
                'frame_number',
                'quantity',
                'reserved',
                'available_quantity'
            )
        }),
        ('Дополнительно', {
            'fields': (
                'description',
                'created_at',
                'updated_at'
            ),
            'classes': ('collapse',)
        }),
    )
    inlines = [ProductImageInline, ProductReviewInline]

    def get_rating(self, obj):
        return obj.get_rating()

    get_rating.short_description = 'Рейтинг'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            from django.utils.html import format_html
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "-"

    image_preview.short_description = "Превью"


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'author', 'rating', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'rating', 'created_at')
    search_fields = ('author', 'text', 'product__model__name')
    list_editable = ('is_approved',)
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'