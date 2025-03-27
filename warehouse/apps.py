from django.apps import AppConfig

# импортируем сигналы
class WarehouseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'warehouse'
    verbose_name = 'Склад'

    def ready(self):
        import warehouse.signals