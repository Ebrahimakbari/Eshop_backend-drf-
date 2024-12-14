from rest_framework import serializers
from .models import (
    Category, Brand, Product, Banners, 
    Cart, CartItem, 
    VisitedProduct, ProductComment
)



class CategorySerializer(serializers.ModelSerializer):        
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'description', 'is_active']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'slug', 'logo']


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), 
        required=False, 
        allow_null=True
    )
    brand = serializers.PrimaryKeyRelatedField(
        queryset=Brand.objects.all(), 
        required=False, 
        allow_null=True
    )
    class Meta:
        model = Product
        fields = [
            'id', 'title', 'slug', 'description', 
            'price', 'category', 
            'brand', 'status', 'inventory', 
            'image', 'views_count', 'is_popular', 
            'created_at', 'updated_at',
        ]
    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("قیمت باید مثبت باشد")
        return value
    
    def validate_inventory(self, value):
        if value < 0:
            raise serializers.ValidationError("موجودی نمی‌تواند منفی باشد")
        return value


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banners
        fields = ['id', 'title', 'url', 'image', 'position', 'is_active']


class CartItemSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title', read_only=True)
    product_price = serializers.DecimalField(source='product.price', read_only=True, max_digits=10, decimal_places=0)
    total_item_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_title', 'product_price', 'quantity', 'total_item_price']

    def get_total_item_price(self, obj):
        return obj.total_price

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("تعداد باید حداقل 1 باشد")
        return value
    
    
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    total_items = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price', 'total_items', 'is_paid']

    def get_total_price(self, obj):
        return obj.total_price()

    def get_total_items(self, obj):
        return obj.total_items()


class VisitedProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = VisitedProduct
        fields = ['id', 'user_ip', 'product', 'user', 'visited_date']


class ProductCommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = ProductComment
        fields = [
            'id', 'product', 'parent', 'user', 
            'created_date', 'text'
        ]