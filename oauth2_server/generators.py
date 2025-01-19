from oauth2_provider.settings import oauth2_settings
from oauthlib.common import generate_token
import jwt
import time
from django.conf import settings


def generate_access_token(request):
    """Generate a JWT access token"""
    expires_in = oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS
    token = generate_token()

    payload = {
        "jti": token,
        "exp": int(time.time()) + expires_in,
        "scope": " ".join(request.scopes),
        "client_id": request.client.client_id,
        "token_type": "access_token",
    }

    # Add user claims if available
    if request.user and request.user.is_authenticated:
        payload.update(
            {
                "sub": str(request.user.id),
                "email": request.user.email,
                "username": request.user.username,
            }
        )

    encoded_token = jwt.encode(
        payload, oauth2_settings.OIDC_RSA_PRIVATE_KEY, algorithm="RS256"
    )
    return encoded_token


def generate_refresh_token(request):
    """Generate a refresh token"""
    return generate_token()
