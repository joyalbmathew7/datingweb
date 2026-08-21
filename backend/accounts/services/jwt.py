from rest_framework_simplejwt.tokens import RefreshToken


class JWTService:
    @staticmethod
    def blacklist_refresh_token(refresh_token):
        token = RefreshToken(refresh_token)
        token.blacklist()