from rest_framework import permissions
from rest_framework.permissions import BasePermission



class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated



class CanProductUpdate(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user==obj.owner




