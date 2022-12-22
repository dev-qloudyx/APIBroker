from rest_framework import permissions
from django.conf import settings

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
    Ensure the request's IP address is authorized.
    """
    def has_permission(self, request, view):
        #remote_addr = request.META['REMOTE_ADDR']
        remote_addr = request.META.get('HTTP_X_FORWARDED_FOR') or request.META['REMOTE_ADDR']
        for ip in settings.AUTHORIZED_IPS_LIST:
            if remote_addr == ip or remote_addr.startswith(ip):
                return True
        return False
        