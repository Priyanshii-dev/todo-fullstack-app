from django.contrib.auth import get_user_model
from rest_framework.views import APIView

from accounts.permissions import IsAdmin
from accounts.serializers.user import UserSerializer, UserStatusSerializer
from todolist.api.responses import error_response, success_response

User = get_user_model()


class UserListAPI(APIView):
    permission_classes = [IsAdmin]      # ← only admin can access

    def get(self, request):
        qs = User.objects.all().order_by("-date_joined")

        status = request.query_params.get("status")
        role   = request.query_params.get("role")

        if status:
            qs = qs.filter(status=status)
        if role:
            qs = qs.filter(role=role)

        return success_response(data=UserSerializer(qs, many=True).data)


class UserStatusUpdateAPI(APIView):
    permission_classes = [IsAdmin]  

    def patch(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return error_response(message="User not found.", status_code=404)

        if user == request.user:
            return error_response(
                message="You cannot change your own status or role.",
                status_code=400,
            )

        serializer = UserStatusSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return success_response(
            data=UserSerializer(user).data,
            message="User updated successfully.",
        )