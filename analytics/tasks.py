from django.utils import timezone
from django.db.models import Count, Sum, Avg, Q
from django.db import transaction, models
from analytics.models import AnalyticsReport
from products.models import Product, ProductReview
from users.models import CustomUser
from warehouse.models import StockMovement


def generate_analytics_report(report_id: int):
    report = AnalyticsReport.objects.get(id=report_id)

    try:
        data = {}

        if report.report_type == 'sales':
            data = generate_sales_report(report)
        elif report.report_type == 'stock':
            data = generate_stock_report(report)
        elif report.report_type == 'users':
            data = generate_users_report(report)
        elif report.report_type == 'reviews':
            data = generate_reviews_report(report)

        with transaction.atomic():
            report.data = data
            report.is_ready = True
            report.save()

    except Exception as e:
        report.data = {'error': str(e)}
        report.save()
        raise


def generate_sales_report(report: AnalyticsReport) -> dict:
    movements = StockMovement.objects.filter(
        movement_type='sale',
        created_at__date__gte=report.period_start,
        created_at__date__lte=report.period_end
    )

    by_day = movements.values('created_at__date').annotate(
        total=Sum('quantity'),
        amount=Sum(models.F('quantity') * models.F('product__price'))
    ).order_by('created_at__date')

    by_product = movements.values('product__model__name').annotate(
        total=Sum('quantity'),
        amount=Sum(models.F('quantity') * models.F('product__price'))
    ).order_by('-amount')

    return {
        'total_sales': movements.aggregate(total=Sum('quantity'))['total'] or 0,
        'total_amount': movements.aggregate(
            amount=Sum(models.F('quantity') * models.F('product__price'))
        )['amount'] or 0,
        'by_day': list(by_day),
        'by_product': list(by_product),
    }


def generate_stock_report(report: AnalyticsReport) -> dict:
    products = Product.objects.filter(
        updated_at__date__lte=report.period_end
    ).annotate(
        movement_count=Count('stockmovement')
    ).order_by('-available_quantity')

    low_stock = products.filter(available_quantity__lte=5)

    return {
        'total_products': products.count(),
        'total_in_stock': products.aggregate(
            total=Sum('available_quantity'))['total'] or 0,
        'low_stock_count': low_stock.count(),
        'low_stock_products': [
            {'id': p.id, 'name': p.model.name, 'quantity': p.available_quantity}
            for p in low_stock
        ],
    }


def generate_reviews_report(report: AnalyticsReport) -> dict:
    reviews = ProductReview.objects.filter(
        created_at__date__gte=report.period_start,
        created_at__date__lte=report.period_end
    )

    by_product = reviews.values('product__model__name').annotate(
        count=Count('id'),
        avg_rating=Avg('rating')
    ).order_by('-avg_rating')

    return {
        'total_reviews': reviews.count(),
        'avg_rating': reviews.aggregate(avg=Avg('rating'))['avg'] or 0,
        'by_product': list(by_product),
        'rating_distribution': list(
            reviews.values('rating').annotate(count=Count('id')).order_by('rating')
        ),
    }


def generate_users_report(report: AnalyticsReport) -> dict:
    """Генерирует отчет о пользователях за указанный период.

    Args:
        report: Объект аналитического отчета

    Returns:
        Словарь с данными отчета:
        - total_users: общее количество пользователей
        - new_users: количество новых пользователей за период
        - active_users: количество активных пользователей (совершали действия)
        - by_type: распределение по типам пользователей
        - by_registration_date: регистрации по дням
    """
    # Общее количество пользователей на конец периода
    total_users = CustomUser.objects.filter(
        date_joined__date__lte=report.period_end
    ).count()

    # Новые пользователи за период
    new_users = CustomUser.objects.filter(
        date_joined__date__gte=report.period_start,
        date_joined__date__lte=report.period_end
    ).count()

    # Активные пользователи (те, кто просматривал товары или оставлял отзывы)
    active_users = CustomUser.objects.filter(
        Q(productview__viewed_at__date__gte=report.period_start) |
        Q(productreview__created_at__date__gte=report.period_start),
        Q(productview__viewed_at__date__lte=report.period_end) |
        Q(productreview__created_at__date__lte=report.period_end)
    ).distinct().count()

    # Распределение по типам пользователей
    by_type = list(
        CustomUser.objects.filter(
            date_joined__date__lte=report.period_end
        ).values('user_type').annotate(
            count=Count('id')
        ).order_by('-count')
    )

    # Регистрации по дням
    by_registration_date = list(
        CustomUser.objects.filter(
            date_joined__date__gte=report.period_start,
            date_joined__date__lte=report.period_end
        ).values('date_joined__date').annotate(
            count=Count('id')
        ).order_by('date_joined__date')
    )

    return {
        'total_users': total_users,
        'new_users': new_users,
        'active_users': active_users,
        'by_type': by_type,
        'by_registration_date': by_registration_date,
        'user_activity': get_user_activity_stats(report)
    }


def get_user_activity_stats(report: AnalyticsReport) -> dict:
    """Дополнительная статистика по активности пользователей."""
    # Топ активных пользователей
    top_active_users = list(
        CustomUser.objects.filter(
            productview__viewed_at__date__gte=report.period_start,
            productview__viewed_at__date__lte=report.period_end
        ).annotate(
            view_count=Count('productview')
        ).order_by('-view_count')[:10].values(
            'id', 'username', 'view_count'
        )
    )

    # Пользователи с отзывами
    users_with_reviews = list(
        CustomUser.objects.filter(
            productreview__created_at__date__gte=report.period_start,
            productreview__created_at__date__lte=report.period_end
        ).annotate(
            review_count=Count('productreview'),
            avg_rating=Avg('productreview__rating')
        ).order_by('-review_count')[:10].values(
            'id', 'username', 'review_count', 'avg_rating'
        )
    )

    return {
        'top_active_users': top_active_users,
        'users_with_reviews': users_with_reviews,
        'users_with_purchases': get_users_with_purchases(report)
    }


def get_users_with_purchases(report: AnalyticsReport) -> list:
    """Получает пользователей с покупками за период."""
    return list(
        CustomUser.objects.filter(
            stockmovement__movement_type='sale',
            stockmovement__created_at__date__gte=report.period_start,
            stockmovement__created_at__date__lte=report.period_end
        ).annotate(
            purchase_count=Count('stockmovement'),
            total_spent=Sum('stockmovement__quantity') * Sum('stockmovement__product__price')
        ).order_by('-total_spent')[:10].values(
            'id', 'username', 'purchase_count', 'total_spent'
        )
    )
