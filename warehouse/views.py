# from django.db.models import Sum, Q, IntegerField, Value, F
# from django.db.models.functions import Coalesce
# from django.views.generic import ListView
# from warehouse.models import Warehouse
#
# class ProductListView(ListView):
#     model = Warehouse
#     template_name = 'products/product_list.html'
#     context_object_name = 'products'
#
#     def get_queryset(self):
#         return Warehouse.objects.annotate(
#             incoming_sum=Coalesce(Sum('product__stock_movements__quantity',
#                 filter=Q(product__stock_movements__movement_type='incoming',
#                          product__stock_movements__status='completed')),
#                 Value(0), output_field=IntegerField()),
#             outgoing_sum=Coalesce(Sum('product__stock_movements__quantity',
#                 filter=Q(product__stock_movements__movement_type__in=['outgoing', 'sale'],
#                          product__stock_movements__status='completed')),
#                 Value(0), output_field=IntegerField()),
#             returns_sum=Coalesce(Sum('product__stock_movements__quantity',
#                 filter=Q(product__stock_movements__movement_type='return',
#                          product__stock_movements__status='completed')),
#                 Value(0), output_field=IntegerField()),
#             calculated_quantity=F('incoming_sum') + F('returns_sum') - F('outgoing_sum')
#         ).filter(calculated_quantity__gt=0)