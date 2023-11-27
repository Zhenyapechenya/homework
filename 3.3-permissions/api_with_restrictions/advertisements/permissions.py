from rest_framework.permissions import BasePermission

class IsOwnerOrReadonly(BasePermission):

    def has_object_permission(self, request, view, obj):
        # Разрешить GET, HEAD или OPTIONS запросы (т.е. только для чтения).
        if request.method in ('GET'):
            return True
        
        # Проверка, является ли пользователь администратором.
        if request.user.is_staff:
            return True

        # Проверка, является ли пользователь владельцем объявления.
        return request.user == obj.creator
