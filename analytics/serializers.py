from rest_framework import serializers
from analytics.models import AnalyticsReport, ProductView
from django.utils import timezone
from datetime import timedelta
from products.models import Product, Category, Manufacturer


class AnalyticsReportSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = AnalyticsReport
        fields = [
            'id', 'report_type', 'period_start', 'period_end',
            'created_at', 'is_ready', 'status', 'data'
        ]
        read_only_fields = ['created_at', 'is_ready', 'data', 'status']

    def get_status(self, obj) -> str:
        return 'Готов' if obj.is_ready else 'В обработке'


class ProductViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductView
        fields = ['id', 'product', 'user', 'viewed_at', 'ip_address']
        read_only_fields = ['viewed_at']


class AnalyticsRequestSerializer(serializers.Serializer):
    report_type = serializers.ChoiceField(choices=AnalyticsReport.REPORT_TYPES)
    period_start = serializers.DateField()
    period_end = serializers.DateField()

    def validate(self, data) -> dict:
        if data['period_start'] > data['period_end']:
            raise serializers.ValidationError("Дата начала периода должна быть раньше даты окончания")

        max_period = timedelta(days=365)
        if (data['period_end'] - data['period_start']) > max_period:
            raise serializers.ValidationError("Максимальный период для анализа - 1 год")

        return data


class AnalyticsDashboardSerializer(serializers.Serializer):
    """Сериализатор для данных аналитического дашборда"""
    total_products = serializers.IntegerField()
    total_categories = serializers.IntegerField()
    total_manufacturers = serializers.IntegerField()
    recent_views = serializers.IntegerField()

    class Meta:
        fields = [
            'total_products',
            'total_categories',
            'total_manufacturers',
            'recent_views'
        ]