from rest_framework import permissions
from django.conf import settings

from apps.users.models import User

class IsAuthenticated(permissions.IsAuthenticated):
    """
    Ensure user is authenticated.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        else:
            return False
          
class HasAdminRole(permissions.BasePermission):
    """
    Ensure user has admin role.
    """
    def has_permission(self, request, view):
        if request.user.role == 1:
            return True
        else:
            return False

class IpAdressPermission(permissions.BasePermission):
    """
    Ensure the request's IP address is the same as user ipAddress.
    """
    def has_permission(self, request, view):
        remote_addr = request.META['REMOTE_ADDR']
        try:
            user = User.objects.get(id=request.user.id)
            if remote_addr == user.ipAddress:
                return True
            else:
                return False
        except:
            return False
        