from django.contrib.auth import get_user_model
from rest_framework import serializers
from accounts.utils.otp import verify_otp

User = get_user_model()


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code  = serializers.CharField(max_length=6, min_length=6)

    def validate(self, attrs):
        email = attrs["email"].strip().lower()
        code  = attrs["code"].strip()

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            raise serializers.ValidationError("No account found with this email.")

        if user.is_email_verified:
            raise serializers.ValidationError("Email is already verified.")

        ok, reason = verify_otp(email, code)
        if not ok:
            raise serializers.ValidationError(reason)

        attrs["user"] = user
        return attrs