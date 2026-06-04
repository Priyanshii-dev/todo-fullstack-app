# from django.contrib.auth.models import User
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
User = get_user_model()
from todolist.serializers import RegisterSerializer
from ..responses import success_response
from .token import get_tokens_for_user


class RegisterAPI(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return success_response(
            data=get_tokens_for_user(user),
            message="Registration successful",
            status_code=201,
        )
