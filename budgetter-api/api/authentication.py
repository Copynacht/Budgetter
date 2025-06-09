from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        access = request.COOKIES.get('access_token')
        if not access:
            return None
        try:
            validated = self.get_validated_token(access)
            return self.get_user(validated), validated
        except Exception:
            raise AuthenticationFailed("Invalid or expired access token")
