from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Cart, CartItem
from products.models import Product


class CartDetailView(LoginRequiredMixin, ListView):
    model = CartItem
    template_name = 'cart/cart_detail.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        cart = Cart.get_cart(self.request.user)
        return CartItem.objects.filter(cart=cart) if cart else []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart.get_cart(self.request.user)
        context['cart'] = cart
        context['total_price'] = cart.total_price if cart else 0
        return context


class CartItemCreateView(LoginRequiredMixin, CreateView):
    model = CartItem
    fields = ['quantity']
    template_name = 'cart/cartitem_form.html'

    def get_success_url(self):
        return reverse_lazy('cart:cart_detail')

    def form_valid(self, form):
        cart = Cart.get_cart(self.request.user)
        product = get_object_or_404(Product, pk=self.kwargs['product_id'])

        # Проверяем, есть ли уже такой товар в корзине
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': form.cleaned_data['quantity']}
        )

        if not created:
            cart_item.quantity += form.cleaned_data['quantity']
            cart_item.save()

        return redirect(self.get_success_url())


class CartItemUpdateView(LoginRequiredMixin, UpdateView):
    model = CartItem
    fields = ['quantity']
    template_name = 'cart/cartitem_form.html'

    def get_queryset(self):
        cart = Cart.get_cart(self.request.user)
        return CartItem.objects.filter(cart=cart)

    def get_success_url(self):
        return reverse_lazy('cart:cart_detail')


class CartItemDeleteView(LoginRequiredMixin, DeleteView):
    model = CartItem
    template_name = 'cart/cartitem_confirm_delete.html'

    def get_queryset(self):
        cart = Cart.get_cart(self.request.user)
        return CartItem.objects.filter(cart=cart)

    def get_success_url(self):
        return reverse_lazy('cart:cart_detail')