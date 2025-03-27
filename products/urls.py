from django.urls import path
from products.views import (
    ProductListView,
    ProductCreateView,
    CategoryCreateView,
    ModelCreateView,
    ManufacturerCreateView,
    ProductDetailView,
    ProductReviewCreateView,
      # Добавлено новое представление
)

app_name = 'products'

urlpatterns = [
    # Основные маршруты для продуктов
    path('', ProductListView.as_view(), name='product_list'),
    path('create/', ProductCreateView.as_view(), name='product_create'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('<int:pk>/add_review/', ProductReviewCreateView.as_view(), name='product_review_create'),

    # Маршруты для категорий
    path('category/create/', CategoryCreateView.as_view(), name='category_create'),
    path('category/<int:pk>/', ProductListView.as_view(), name='category_products'),  # Новый маршрут

    # Маршруты для моделей и производителей
    path('model/create/', ModelCreateView.as_view(), name='model_create'),
    path('manufacturer/create/', ManufacturerCreateView.as_view(), name='manufacturer_create'),
]