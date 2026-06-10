import logging

from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.views import APIView
from accounts.utils.otp import send_otp
from todolist.api.responses import success_response

User = get_user_model()
logger = logging.getLogger(__name__)


class ResendOTPAPI(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email", "").strip().lower()
        user  = User.objects.filter(email__iexact=email).first()

        # Always return 200 — don't leak whether email exists
        if user and not user.is_email_verified:
            try:
                send_otp(user)
                logger.info("Resend OTP sent to %s", user.email)
            except Exception as e:
                logger.error("Failed to resend OTP to %s: %s", user.email, e)

        return success_response(
            data=None,
            message="If that email exists and is unverified, a new OTP has been sent.",
        )