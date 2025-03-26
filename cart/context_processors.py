from .models import Cart

def cart(request):
    return {
        'cart': Cart.get_cart(request.user) if request.user.is_authenticated else None
    }