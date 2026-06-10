# accounts/api/verify_otp.py

from rest_framework import permissions
from rest_framework.views import APIView
from accounts.serializers.otp import VerifyOTPSerializer
from todolist.api.responses import success_response


class VerifyOTPAPI(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]  # ← only user, no otp object

        # Mark email verified — OTP already deleted from Redis in serializer
        user.is_email_verified = True
        user.save(update_fields=["is_email_verified"])

        return success_response(
            data=None,
            message="Email verified successfully. Await admin approval.",
        )