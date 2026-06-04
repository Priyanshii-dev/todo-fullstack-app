from django.contrib.auth import authenticate
from rest_framework import permissions
from rest_framework.views import APIView

from accounts.serializers.login import LoginSerializer
from accounts.api.token import get_tokens_for_user
from todolist.api.responses import error_response, success_response


class LoginAPI(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            request=request,
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        if user is None:
            return error_response(
                message="Invalid email or password.",
                status_code=401,
            )

        return success_response(
            data=get_tokens_for_user(user),
            message="Login successful",
        )
