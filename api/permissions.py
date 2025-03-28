from rest_framework import permissions

class IsAdminOrSelf(permissions.BasePermission):
    def has_permission(self, request, view):
        # Разрешение доступа к списку только администраторам
        if request.method == 'GET' and view.action == 'list':
            return request.user.is_admin()
        return True  # Разрешаем другие методы (POST, PUT, DELETE) для всех авторизованных пользователей

    def has_object_permission(self, request, view, obj):
        # Разрешение доступа к конкретному объекту только администратору или самому пользователю
        return request.user.is_admin() or request.user == obj

