from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Кастомное право доступа:
    - Читать (GET, HEAD, OPTIONS) могут все
    - Создавать/Изменять/Удалять (POST, PUT, PATCH, DELETE) могут только админы
    """
    
    def has_permission(self, request, view):
        # Безопасные методы (чтение) разрешены всем
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Для изменений нужно быть авторизованным И быть админом
        return request.user and request.user.is_authenticated and request.user.is_staff
    