from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class ProductPagination(PageNumberPagination):
    """
    Кастомная пагинация для товаров
    
    Примеры использования:
    /api/products/ - первая страница (20 товаров)
    /api/products/?page=2 - вторая страница
    /api/products/?page=1&page_size=10 - 10 товаров на странице
    /api/products/?page=1&page_size=50 - 50 товаров на странице
    """
    page_size = 20  
    page_size_query_param = 'page_size'  
    max_page_size = 100  
    page_query_param = 'page' 
    
    def get_paginated_response(self, data):
        """
        Кастомный формат ответа с дополнительной информацией
        """
        return Response({
            'count': self.page.paginator.count,  
            'total_pages': self.page.paginator.num_pages, 
            'current_page': self.page.number, 
            'page_size': self.get_page_size(self.request),  
            'next': self.get_next_link(), 
            'previous': self.get_previous_link(),  
            'results': data 
        })
