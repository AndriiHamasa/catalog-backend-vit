from rest_framework import serializers
from .models import Category, Product, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий"""
    product_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'title', 'product_count', 'created_at']
    
    def get_product_count(self, obj):
        return obj.products.filter(is_active=True).count()


# class ProductImageSerializer(serializers.ModelSerializer):
#     """Сериализатор для изображений"""
#     class Meta:
#         model = ProductImage
#         fields = ['id', 'image', 'order']

class ProductImageSerializer(serializers.ModelSerializer):
    """Сериализатор для изображений"""
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'order']
    
    def get_image(self, obj):
        """Возвращает URL изображения (из файла или URL поля)"""
        return obj.get_image_url()


class ProductListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка товаров (краткая информация)"""
    category_name = serializers.CharField(source='category.title', read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 
            'title', 
            'category', 
            'category_name', 
            'price', 
            'status',
            'status_display',
            'images', 
            'created_at'
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детальной информации о товаре"""
    category_name = serializers.CharField(source='category.title', read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 
            'title', 
            'category', 
            'category_name',
            'description', 
            'price', 
            'status',
            'status_display',
            'is_active',
            'images', 
            'created_at',
            'updated_at'
        ]