from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_site_admin: 
            return True
        return False
    def has_object_permission(self, request, view, obj):
        if request.user.is_site_admin:
            
            return True

