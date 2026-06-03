from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import Task


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username", "email"]


class TaskSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "task",
            "is_completed",
            "user_id",
            "email",
        ]
        read_only_fields = ["user_id", "email"]

    def validate_task(self, value):

        value = value.strip()
        if not value:
            raise serializers.ValidationError(
                "Task cannot be empty."
            )

        return value


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, trim_whitespace=False)

    class Meta:

        model = User
        fields = ["email", "password"]

    def validate_email(self, value):
        value = value.strip().lower()

        if not value:
            raise serializers.ValidationError(
                "Email is required."
            )

        # Check both username and email
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError(
                "Email already registered."
            )

        return value

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        email = validated_data["email"]
        return User.objects.create_user(
            username=email,
            email=email,
            password=validated_data["password"],
        )


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
