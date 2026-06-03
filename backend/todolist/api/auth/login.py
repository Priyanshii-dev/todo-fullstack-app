from django.contrib.auth import authenticate
from rest_framework import permissions
from rest_framework.views import APIView

from todolist.serializers import LoginSerializer
from ..responses import error_response, success_response
from .token import get_tokens_for_user


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
