from rest_framework import permissions  # наш личный permission

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS: # (GET, HEAD, OPTIONS)
            return True  # если метод безопасный - можно всем, иначе только админам
        
        return bool(request.user and request.user.is_staff)  # from permissions.IsAdminUser
    
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user
