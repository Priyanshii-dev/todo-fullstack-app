from rest_framework.views import APIView

from accounts.permissions import IsEmployee
from accounts.serializers.user import UserSerializer
from todolist.api.responses import success_response


class EmployeeDashboardAPI(APIView):
    """Employee-only view. Blocked for admins and pending/rejected users."""
    permission_classes = [IsEmployee]

    def get(self, request):
        return success_response(
            data=UserSerializer(request.user).data,
            message=f"Welcome, {request.user.email}!",
        )