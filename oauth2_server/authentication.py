from django.http import HttpRequest
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
import jwt
from django.contrib.auth import get_user_model
from config.settings import PUBLIC_KEY
from rest_framework.authentication import get_authorization_header
from django.utils.translation import gettext as _


class TurboOAuth2Authentication(BaseAuthentication):

    keyword = "Turbo"

    def authenticate(self, request):

        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = _("Invalid token header. No credentials provided.")
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _("Invalid token header. Token string should not contain spaces.")
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _(
                "Invalid token header. Token string should not contain invalid characters."
            )
            raise exceptions.AuthenticationFailed(msg)

        user, token, payload = self.authenticate_credentials(token)

        request.validated_payload = payload

        return (user, token)

    def authenticate_credentials(self, token: str):
        User = get_user_model()

        try:
            payload = self._decode_jwt(token)

            user = User.objects.get(id=payload["sub"])

            if not user.is_active:
                raise exceptions.AuthenticationFailed("User inactive or deleted")

            return user, token, payload

        except jwt.ExpiredSignatureError as e:
            raise exceptions.AuthenticationFailed("Token has expired")
        except jwt.InvalidTokenError as e:
            raise exceptions.AuthenticationFailed("Invalid token")
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("User not found")
        except Exception as e:
            raise exceptions.AuthenticationFailed("Authentication failed")

    def authenticate_header(self, request):
        return self.keyword

    def _decode_jwt(self, token: str) -> dict:
        try:
            payload = jwt.decode(
                token,
                PUBLIC_KEY,
                algorithms=["RS256"],
                options={
                    "verify_aud": True,
                    "verify_iss": True,
                    "verify_exp": True,
                    "verify_iat": True,
                },
            )
            return payload
        except Exception as e:
            raise
