from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False
    )

    def validate_email(self, value):
        value = value.strip().lower()
        if not value:
            raise serializers.ValidationError(
                "Email is required."
            )

        return value

    def validate(self, attrs):
        email    = attrs.get("email")
        password = attrs.get("password")

        user = User.objects.filter(email__iexact=email).first()

        if user is None:
            raise serializers.ValidationError("No account found with this email.")
        if not user.check_password(password):
            raise serializers.ValidationError("Incorrect password.")
        if not user.is_active:
            raise serializers.ValidationError("This account is deactivated.")

        attrs["user"] = user
        return attrs
