from rest_framework import generics, permissions
from django.contrib.auth import get_user_model

from accounts.serializers.register import RegisterSerializer
from todolist.api.responses import success_response

User = get_user_model()


class RegisterAPI(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()                   # ← don't capture user

        return success_response(
            data=None,                      # ← no tokens returned
            message="Registration successful. Your account is pending admin approval.",
            status_code=201,
        )