from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from oauth2_provider.views import AuthorizationView as BaseAuthorizationView
from oauth2_provider.models import get_application_model
from oauth2_provider.exceptions import OAuthToolkitError
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from .authentication import TurboOAuth2Authentication
from .permissions import IsTurboOAuth2Authenticated


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
    permission_classes = [IsTurboOAuth2Authenticated]

    def get(self, request, *args, **kwargs):
        token_payload = (
            request.validated_token_payload
            if hasattr(request, "validated_token_payload")
            else None
        )
        claims = {
            "sub": str(token_payload["sub"]),
        }

        if token_payload and "profile" in token_payload["scope"]:
            claims.update(
                {
                    "email": token_payload["email"],
                    "username": token_payload["username"],
                    "name": token_payload["name"],
                }
            )

        return Response(claims)
