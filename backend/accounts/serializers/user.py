from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ["id", "email", "role", "status"]


class UserStatusSerializer(serializers.ModelSerializer):
    """Admin-only: change a user's status or role."""
    class Meta:
        model  = User
        fields = ["status"]

    def validate_status(self, value):
        allowed = [s.value for s in User.Status]
        if value not in allowed:
            raise serializers.ValidationError(
                f"Status must be one of: {allowed}"
            )
        return value

    def validate_role(self, value):
        allowed = [r.value for r in User.Role]
        if value not in allowed:
            raise serializers.ValidationError(
                f"Role must be one of: {allowed}"
            )
        return value