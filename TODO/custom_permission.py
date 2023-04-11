from rest_framework.permissions import BasePermission


class IsAuthorOrAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):
        """
        Determine if the user has permission to edit the task.
        Only author or admin can delete task.
        """
        if request.user.is_authenticated:
            if request.user == obj.author or request.user.is_staff:
                return True
        return False
