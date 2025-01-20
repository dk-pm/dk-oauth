from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from oauth2_provider.views import AuthorizationView as BaseAuthorizationView
from oauth2_provider.models import get_application_model
from oauth2_provider.exceptions import OAuthToolkitError
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from .authentication import TurboOAuth2Authentication
from .permissions import IsTurboOAuth2Authenticated
from .models import DigikalaUser
from .auth import DigikalaAuthBackend
from django.conf import settings
from urllib.parse import quote


class DigikalaAuthorizationView(BaseAuthorizationView):
    template_name = "oauth2_server/authorize.html"

    def dispatch(self, request, *args, **kwargs):
        # Get all original OAuth2 parameters
        oauth2_params = {
            'client_id': request.GET.get('client_id'),
            'redirect_uri': request.GET.get('redirect_uri'),
            'response_type': request.GET.get('response_type'),
            'scope': request.GET.get('scope'),
            'state': request.GET.get('state'),
            'code_challenge': request.GET.get('code_challenge'),
            'code_challenge_method': request.GET.get('code_challenge_method'),
        }
        
        # Create the return URL with all OAuth2 parameters
        return_url_params = '&'.join([f'{k}={v}' for k, v in oauth2_params.items() if v])
        return_url = f'/campaigns/oauth/authorize/?{return_url_params}'
        encoded_return_url = quote(return_url)
        
        digikala_token = request.COOKIES.get('Digikala:User:Token:new')
        login_token = request.GET.get('login_token')
        
        if login_token:
            return redirect(f'{settings.DIGIKALA_LOGIN_URL}?backUrl={encoded_return_url}&login_token={login_token}')
        
        if not digikala_token:
            return redirect(f'{settings.DIGIKALA_LOGIN_URL}?backUrl={encoded_return_url}')
            
        # Authenticate with Digikala
        auth_backend = DigikalaAuthBackend()
        user = auth_backend.authenticate(request, digikala_token=digikala_token)
        
        if not user:
            return redirect(f'{settings.DIGIKALA_LOGIN_URL}?backUrl={encoded_return_url}')
            
        request.user = user
        return super().dispatch(request, *args, **kwargs)

    def store_oauth2_params(self, request):
        """Store OAuth2 parameters in session"""
        oauth2_params = {
            'client_id': request.GET.get('client_id'),
            'redirect_uri': request.GET.get('redirect_uri'),
            'response_type': request.GET.get('response_type'),
            'scope': request.GET.get('scope'),
            'state': request.GET.get('state'),
            'code_challenge': request.GET.get('code_challenge'),
            'code_challenge_method': request.GET.get('code_challenge_method'),
        }
        request.session['oauth2_params'] = oauth2_params

    def get_scopes(self):
        scope_string = self.request.GET.get("scope", "")
        if not scope_string and hasattr(self, "oauth2_data"):
            scope_string = self.oauth2_data.get("scope", "")
        return scope_string.split() if scope_string else []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
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

            scopes = self.get_scopes()
            if isinstance(scopes, list):
                scopes = " ".join(scopes)

            uri = self.create_authorization_response(
                request=self.request,
                scopes=scopes,
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


class DigikalaUserInfoView(APIView):
    authentication_classes = [TurboOAuth2Authentication]
    permission_classes = [IsTurboOAuth2Authenticated]

    def get(self, request, *args, **kwargs):
        token_payload = request.validated_token_payload if hasattr(request, "validated_token_payload") else None
        if not token_payload:
            return Response({"error": "Invalid token"}, status=401)

        try:
            user = DigikalaUser.objects.get(digikala_id=token_payload["sub"])
        except DigikalaUser.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        claims = {
            "sub": str(user.digikala_id),
        }

        if "profile" in token_payload.get("scope", "").split():
            claims.update({
                "name": user.full_name,
                "given_name": user.first_name,
                "family_name": user.last_name,
                "email": user.email,
                "phone_number": user.mobile,
            })

        return Response(claims)
