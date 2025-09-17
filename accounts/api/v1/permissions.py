from rest_framework.permissions import BasePermission

class IsAnonymousUser(BasePermission):
    """ just anonymous user access """

    def has_permission(self, request, view):
        return not request.user or request.user.is_anonymous
