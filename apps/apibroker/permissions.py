from rest_framework import permissions

class IsAuthenticated(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        else:
            return False
          
class HasAdminRole(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 1:
            return True
        else:
            return False