from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product
from .serializers import (
    CategorySerializer, 
    ProductListSerializer, 
    ProductDetailSerializer
)
from .permissions import IsAdminOrReadOnly
from .pagination import ProductPagination 


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API для категорий - полный CRUD
    GET /api/categories/ - список всех категорий (доступно всем)
    POST /api/categories/ - создать категорию (только админ)
    GET /api/categories/{id}/ - получить категорию (доступно всем)
    PUT /api/categories/{id}/ - обновить категорию (только админ)
    DELETE /api/categories/{id}/ - удалить категорию (только админ)
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]  # Защита!
    pagination_class = None
    
    def destroy(self, request, *args, **kwargs):
        """Удаление категории"""
        instance = self.get_object()
        # Можно добавить проверку, есть ли товары в категории
        product_count = instance.products.count()
        if product_count > 0:
            return Response(
                {'error': f'Невозможно удалить категорию. В ней {product_count} товар(ов)'},
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductViewSet(viewsets.ModelViewSet):
    """
    API для товаров - полный CRUD
    GET /api/products/ - список всех товаров (доступно всем)
    POST /api/products/ - создать товар (только админ)
    GET /api/products/{id}/ - получить товар (доступно всем)
    PUT /api/products/{id}/ - обновить товар (только админ)
    PATCH /api/products/{id}/ - частично обновить товар (только админ)
    DELETE /api/products/{id}/ - удалить товар (только админ)
    
    Фильтры:
    GET /api/products/?category=1 - по категории
    GET /api/products/?status=new - по статусу
    GET /api/products/?search=название - поиск
    """
    queryset = Product.objects.all().select_related('category').prefetch_related('images')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'status', 'is_active']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title', 'price']
    ordering = ['-created_at']
    permission_classes = [IsAdminOrReadOnly]  # Защита!
    pagination_class = ProductPagination 
    
    def get_queryset(self):
        """Для списка показываем только активные, для админки - все"""
        queryset = super().get_queryset()
        # Если хочешь показывать только активные товары, раскомментируй:
        # if self.action == 'list':
        #     queryset = queryset.filter(is_active=True)
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """
        Получить товары по ID категории
        GET /api/products/by_category/?category_id=1
        """
        category_id = request.query_params.get('category_id')
        if not category_id:
            return Response({'error': 'ID категории не указан'}, status=400)
        
        queryset = self.filter_queryset(self.get_queryset().filter(category_id=category_id))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
        # products = self.get_queryset().filter(category_id=category_id)
        # serializer = self.get_serializer(products, many=True)
        # return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def new_arrivals(self, request):
        """
        Получить новые поставки
        GET /api/products/new_arrivals/
        """
        # products = self.get_queryset().filter(status='new', is_active=True)
        # serializer = self.get_serializer(products, many=True)
        # return Response(serializer.data)
        queryset = self.filter_queryset(self.get_queryset().filter(status='new', is_active=True))
        
        # Применяем пагинацию
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        """
        Переключить активность товара
        POST /api/products/{id}/toggle_active/
        """
        product = self.get_object()
        product.is_active = not product.is_active
        product.save()
        serializer = self.get_serializer(product)
        return Response(serializer.data)
