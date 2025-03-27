from django.urls import path
from .views import (
    CartDetailView,
    CartItemCreateView,
    CartItemUpdateView,
    CartItemDeleteView
)

app_name = 'cart'

urlpatterns = [
    path('', CartDetailView.as_view(), name='cart_detail'),
    path('add/<int:product_id>/', CartItemCreateView.as_view(), name='cart_item_add'),
    path('update/<int:pk>/', CartItemUpdateView.as_view(), name='cart_item_update'),
    path('delete/<int:pk>/', CartItemDeleteView.as_view(), name='cart_item_delete'),
]