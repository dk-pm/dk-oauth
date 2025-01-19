from rest_framework.permissions import BasePermission


class IsTurboOAuth2Authenticated(BasePermission):

    def has_permission(self, request, view):
        print(request.validated_token_payload)
        if hasattr(request, "validated_token_payload"):
            return True
        return False
