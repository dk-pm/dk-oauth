from django.urls import path, include
from oauth2_provider.views import (
    TokenView,
    RevokeTokenView,
    IntrospectTokenView,
    ConnectDiscoveryInfoView,
    JwksInfoView,
)
from .views import AuthorizationView, UserInfoView

app_name = "oauth2_provider"

urlpatterns = [
    # OAuth2 endpoints
    path("authorize/", AuthorizationView.as_view(), name="authorize"),
    path("token/", TokenView.as_view(), name="token"),
    path("revoke/", RevokeTokenView.as_view(), name="revoke-token"),
    path("introspect/", IntrospectTokenView.as_view(), name="introspect"),
    # OpenID Connect endpoints
    path("userinfo/", UserInfoView.as_view(), name="userinfo"),
    path(
        ".well-known/openid-configuration/",
        ConnectDiscoveryInfoView.as_view(),
        name="oidc-connect-discovery-info",
    ),
    path(".well-known/jwks.json", JwksInfoView.as_view(), name="jwks-info"),
]
