from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from oauth2_provider.views import AuthorizationView as BaseAuthorizationView
from oauth2_provider.models import get_application_model
from oauth2_provider.exceptions import OAuthToolkitError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .authentication import TurboOAuth2Authentication


class AuthorizationView(BaseAuthorizationView, LoginRequiredMixin):
    template_name = "oauth2_server/authorize.html"
    login_url = "/accounts/login/"

    def get_scopes(self):
        # Get scopes from the request query parameters
        scope_string = self.request.GET.get("scope", "")
        if not scope_string and hasattr(self, "oauth2_data"):
            # Fallback to oauth2_data if available
            scope_string = self.oauth2_data.get("scope", "")
        return scope_string.split() if scope_string else []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the application
        application = None
        try:
            application = get_application_model().objects.get(
                client_id=self.oauth2_data.get("client_id")
            )
            context["application"] = application
        except get_application_model().DoesNotExist:
            pass

        scopes = self.get_scopes()

        scope_descriptions = {
            "openid": "Access your basic profile information",
            "profile": "Access to your full profile details",
            "email": "Access your email address",
        }

        context["scopes_descriptions"] = [
            scope_descriptions.get(scope, scope) for scope in scopes
        ]
        return context

    @transaction.atomic
    def form_valid(self, form):
        try:
            credentials = {
                "client_id": form.cleaned_data.get("client_id"),
                "redirect_uri": form.cleaned_data.get("redirect_uri"),
                "response_type": form.cleaned_data.get("response_type", None),
                "state": form.cleaned_data.get("state", None),
                "scope": form.cleaned_data.get("scope", None),
                "code_challenge": form.cleaned_data.get("code_challenge", None),
                "code_challenge_method": form.cleaned_data.get(
                    "code_challenge_method", None
                ),
            }

            allow = form.cleaned_data.get("allow", False)
            if not allow:
                redirect_url = self.error_response(credentials, "access_denied")
                return HttpResponseRedirect(redirect_url)

            # Convert scopes list to space-separated string if needed
            scopes = self.get_scopes()
            if isinstance(scopes, list):
                scopes = " ".join(scopes)

            uri = self.create_authorization_response(
                request=self.request,
                scopes=scopes,  # Now passing a string instead of a list
                credentials=credentials,
                allow=True,
            )[0]
            return HttpResponseRedirect(uri)

        except OAuthToolkitError as error:
            redirect_url = self.error_response(error.credentials, error.error)
            return HttpResponseRedirect(redirect_url)


class UserInfoView(APIView):
    authentication_classes = [TurboOAuth2Authentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        claims = {
            "sub": str(user.id),
            "name": user.get_full_name(),
            "preferred_username": user.username,
            "email": user.email,
            "email_verified": True,
        }

        # Add profile claims if scope is present
        payload = (
            request.validated_payload if hasattr(request, "validated_payload") else None
        )

        if payload and "profile" in payload["scope"]:
            claims.update(
                {
                    "given_name": user.first_name,
                    "family_name": user.last_name,
                }
            )

        return Response(claims)
