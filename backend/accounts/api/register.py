from rest_framework import generics, permissions
from django.contrib.auth import get_user_model

from accounts.serializers.register import RegisterSerializer
from accounts.api.token import get_tokens_for_user
from todolist.api.responses import success_response

User = get_user_model()


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
