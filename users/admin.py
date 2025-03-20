from django.contrib import admin
from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'user_type', 'date_joined', 'is_active')
    list_filter = ('user_type', 'is_active', 'date_joined')
    search_fields = ['username', 'email', 'phone']
    readonly_fields = ('date_joined', 'last_login')
    fieldsets = (
        ('Основная информация', {
            'fields': ('username', 'email', 'phone', 'password')
        }),
        ('Персональная информация', {
            'fields': ('avatar', 'bio', 'date_of_birth')
        }),
        ('Права доступа', {
            'fields': ('user_type', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Важные даты', {
            'fields': ('last_login', 'date_joined')
        }),
    )
