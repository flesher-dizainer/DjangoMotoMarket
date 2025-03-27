from django.urls import path
from products.views import (
    ProductListView,
    ProductCreateView,
    CategoryCreateView,
    ModelCreateView,
    ManufacturerCreateView,
    ProductDetailView,
    # Добавлено новое представление
)

app_name = 'products'

urlpatterns = [
    # Основные маршруты для продуктов
    path('', ProductListView.as_view(), name='product_list'),
    path('create/', ProductCreateView.as_view(), name='product_create'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),

    # Маршруты для категорий
    path('category/create/', CategoryCreateView.as_view(), name='category_create'),

    # Маршруты для моделей и производителей
    path('model/create/', ModelCreateView.as_view(), name='model_create'),
    path('manufacturer/create/', ManufacturerCreateView.as_view(), name='manufacturer_create'),
]
