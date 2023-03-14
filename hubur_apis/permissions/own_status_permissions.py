from rest_framework import permissions

class UpdateOwnStatus(permissions.BasePermission):
    """ Allow user to update their own profile """

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True
        
        try:
            return obj.user.id == request.user.id
        except Exception:
            return obj.id.id == request.user.id

