# analytics/middleware.py
from django.utils import timezone
from .models import ProductView
from products.models import Product


class ProductViewMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.path.startswith('/products/') and request.method == 'GET':
            try:
                # Извлекаем ID товара из URL (пример: /products/123/)
                product_id = request.path.split('/')[2]
                if product_id.isdigit():
                    product = Product.objects.get(id=product_id)
                    ProductView.objects.create(
                        product=product,
                        user=request.user if request.user.is_authenticated else None,
                        ip_address=self.get_client_ip(request)
                    )
            except (IndexError, Product.DoesNotExist):
                pass

        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')