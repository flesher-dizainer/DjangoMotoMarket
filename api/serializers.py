from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.models import Sum
from rest_framework import serializers
from users.models import CustomUser
from products.models import Category, Manufacturer, Model, Product, ProductImage, ProductReview
from warehouse.models import StockMovement


class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    avatar_url = serializers.SerializerMethodField(read_only=True)
    is_admin = serializers.SerializerMethodField(read_only=True)
    is_manager = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'url', 'id', 'username', 'email', 'first_name', 'last_name',
            'user_type', 'phone', 'avatar', 'avatar_url', 'bio',
            'date_of_birth', 'is_admin', 'is_manager', 'password'
        ]
        extra_kwargs = {
            'url': {'lookup_field': 'username'},
            'password': {'write_only': True, 'required': False},  # Пароль только для записи
            'avatar': {'required': False}  # Аватар не обязателен
        }
        read_only_fields = ['id', 'is_admin', 'is_manager', 'avatar_url', 'user_type']

    def get_avatar_url(self, obj) -> str | None:
        request = self.context.get('request')
        if obj.avatar and hasattr(obj.avatar, 'url'):
            if request:
                return request.build_absolute_uri(obj.avatar.url)
            return obj.avatar.url
        return None

    def get_is_admin(self, obj) -> bool:
        return obj.is_staff or obj.is_superuser

    def get_is_manager(self, obj) -> bool:
        return obj.user_type == 'manager'  # Предполагая, что есть такой user_type

    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Invalid email format")
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate_username(self, value) -> str:
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class UserRegistrationSerializer(CustomUserSerializer):
    class Meta(CustomUserSerializer.Meta):
        extra_kwargs = {
            **CustomUserSerializer.Meta.extra_kwargs,
            'password': {'write_only': True, 'required': True},  # Пароль обязателен при регистрации
            'email': {'required': True},  # Email обязателен
            'username': {'required': True}  # Имя пользователя обязательно
        }

    def validate(self, data):
        # Дополнительные проверки для регистрации
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if not data.get(field):
                raise serializers.ValidationError({field: "This field is required"})
        return data


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['url', 'id', 'name']
        extra_kwargs = {
            'url': {'view_name': 'category-detail', 'lookup_field': 'pk'}
        }


class ManufacturerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ['url', 'id', 'name']
        extra_kwargs = {
            'url': {'view_name': 'manufacturer-detail', 'lookup_field': 'pk'}
        }


class ModelSerializer(serializers.HyperlinkedModelSerializer):
    manufacturer = ManufacturerSerializer()

    class Meta:
        model = Model
        fields = ['url', 'id', 'manufacturer', 'name']
        extra_kwargs = {
            'url': {'view_name': 'model-detail', 'lookup_field': 'pk'}
        }


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = ['id', 'author', 'text', 'rating', 'created_at']


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    category = CategorySerializer()
    model = ModelSerializer()
    images = ProductImageSerializer(many=True, read_only=True)
    reviews = ProductReviewSerializer(many=True, read_only=True)
    available_quantity = serializers.IntegerField(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'url',
            'id',
            'category',
            'model',
            'year',
            'engine_capacity',
            'price',
            'color',
            'front_wheel_size',
            'rear_wheel_size',
            'frame_number',
            'description',
            'quantity',
            'reserved',
            'available_quantity',
            'created_at',
            'updated_at',
            'images',
            'reviews',
            'rating',
        ]
        extra_kwargs = {
            'url': {'view_name': 'product-detail', 'lookup_field': 'pk'}
        }

    def get_rating(self, obj) -> float:
        return obj.get_rating()


class StockMovementSerializer(serializers.HyperlinkedModelSerializer):
    product = ProductSerializer(read_only=True)
    product_url = serializers.HyperlinkedRelatedField(
        source='product',
        view_name='product-detail',
        lookup_field='pk',
        queryset=Product.objects.all(),
        write_only=True
    )
    current_stock = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = StockMovement
        fields = [
            'url', 'id', 'product', 'product_url', 'movement_type', 'quantity',
            'status', 'created_at', 'comment', 'current_stock'
        ]
        extra_kwargs = {
            'url': {'view_name': 'stockmovement-detail', 'lookup_field': 'pk'},
        }

    def get_current_stock(self, obj) -> int:
        # Вычисляем текущий остаток товара
        incoming = StockMovement.objects.filter(
            product=obj.product,
            movement_type__in=['incoming', 'return'],
            status='completed'
        ).aggregate(Sum('quantity'))['quantity__sum'] or 0

        outgoing = StockMovement.objects.filter(
            product=obj.product,
            movement_type__in=['outgoing', 'sale'],
            status='completed'
        ).aggregate(Sum('quantity'))['quantity__sum'] or 0

        return incoming - outgoing

    def validate(self, data):
        if self.instance and self.instance.status == 'completed':
            raise serializers.ValidationError("Нельзя изменять выполненное движение")
        return data

    def create(self, validated_data):
        # Удаляем product_url из validated_data, так как он используется только для записи
        validated_data.pop('product_url', None)
        return super().create(validated_data)
