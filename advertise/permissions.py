from rest_framework import permissions


class IsImageOwner(permissions.BasePermission):
    message = "you aren\'t owner of this ad"

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


class IsProfileComplete(permissions.BasePermission):
    message = "your must complete your personal info (first name, last_name, address)"

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        user = request.user
        return user.first_name and user.last_name and user.address
