from rest_framework import permissions


class IsImageOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        is_owner = obj.advertise.user == request.user
        return request.user.is_authenticated and is_owner


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_authenticated

        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user
