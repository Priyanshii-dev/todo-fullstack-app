from rest_framework_simplejwt.tokens import RefreshToken

from accounts.serializers.user import UserSerializer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "token": str(refresh.access_token),
        "user": UserSerializer(user).data,
    }
