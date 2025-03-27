from django import forms
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .forms import ProductForm, ReviewForm
from .models import Product, Category, Manufacturer, Model, ProductImage, ProductReview


# Продукт
class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all().only('name', 'pk')
        context['manufacturers'] = Manufacturer.objects.all().only('name', 'pk')
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        request = self.request
        search_query = request.GET.get('search')
        category_id = request.GET.get('category')
        manufacturer_id = request.GET.get('manufacturer')
        price_min = request.GET.get('price_min')  # Получаем минимальную цену
        price_max = request.GET.get('price_max')  # Получаем максимальную цену

        # Фильтрация по поисковому запросу (если есть)
        if search_query:
            queryset = queryset.filter(
                Q(model__name__icontains=search_query) |
                Q(model__manufacturer__name__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        # Фильтрация по категории (если выбрана)
        if category_id:
            queryset = queryset.filter(category__pk=category_id)

        # Фильтрация по производителю (если выбран)
        if manufacturer_id:
            queryset = queryset.filter(model__manufacturer__pk=manufacturer_id)

        # 🔥 Фильтрация по диапазону цен (если указаны min или max)
        if price_min:
            queryset = queryset.filter(price__gte=float(price_min))  # price >= price_min
        if price_max:
            queryset = queryset.filter(price__lte=float(price_max))  # price <= price_max

        # Оптимизация запросов к связанным моделям
        return queryset.select_related('category', 'model', 'model__manufacturer')


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('products:product_list')

    def form_valid(self, form):
        # Сначала сохраняем продукт
        self.object = form.save()

        # Затем обрабатываем изображения
        images = self.request.FILES.getlist('images')
        for image in images:
            ProductImage.objects.create(product=self.object, image=image)

        return super().form_valid(form)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'  # для удобства, чтобы не писать product = self.object в шаблоне

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.reviews.filter(is_approved=True)
        context['review_form'] = ReviewForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = self.object
            review.author = request.POST.get('author', 'Anonymous')  # обработка автора, по умолчанию Аноним
            review.save()
            messages.success(request, 'Ваш отзыв успешно отправлен на модерацию!')  # сообщение об успехе
            return redirect(self.object)  # Перенаправляем на страницу товара
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')  # сообщение об ошибке
            context = self.get_context_data(**kwargs)
            context['review_form'] = form  # Передаем форму с ошибками в контекст
            return self.render_to_response(context)


# Category
class CategoryCreateView(CreateView):
    model = Category
    fields = ['name']
    success_url = reverse_lazy('products:product_create')
    template_name = 'products/category_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# Model
class ModelCreateView(CreateView):
    model = Model
    fields = ['manufacturer', 'name']
    success_url = reverse_lazy('products:product_create')
    template_name = 'products/model_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head_text'] = 'модели'
        context['model'] = True
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# manufacturer
class ManufacturerCreateView(CreateView):
    model = Manufacturer
    fields = ['name']
    success_url = reverse_lazy('products:model_create')
    template_name = 'products/model_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head_text'] = 'производителя'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


