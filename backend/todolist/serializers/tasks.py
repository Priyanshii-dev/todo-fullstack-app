from rest_framework import serializers

from ..models import Task


class TaskSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    logo = serializers.SerializerMethodField()
    logo_upload = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = Task
        fields = [
            "id",
            "task",
            "is_completed",
            "user_id",
            "email",
            "logo",
            "logo_upload",
        ]
        read_only_fields = ["user_id", "email"]

    def get_logo(self, obj):
        if not obj.logo:
            return None
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(f"/api/tasks/{obj.id}/logo/")
        return f"/api/tasks/{obj.id}/logo/"

    def validate_task(self, value):

        value = value.strip()
        if not value:
            raise serializers.ValidationError("Task cannot be empty.")
        request = self.context.get("request")
        if request and request.user:
            task_id = self.instance.id if self.instance else None
            if Task.objects.filter(
                user=request.user,
                task__iexact=value
            ).exclude(id=task_id).exists():
                raise serializers.ValidationError("You already have a task with this name.")
        return value

    def validate(self, attrs):
        if not self.instance and attrs.get("is_completed"):
            raise serializers.ValidationError("A new task cannot be marked as completed.")
        return attrs

    def update(self, instance, validated_data):
        logo_file = validated_data.pop("logo_upload", None)
        if logo_file is not None:
            instance.logo = logo_file.read()
            instance.logo_content_type = logo_file.content_type or "image/png"
        return super().update(instance, validated_data)

    def create(self, validated_data):
        logo_file = validated_data.pop("logo_upload", None)
        if logo_file is not None:
            validated_data["logo"] = logo_file.read()
            validated_data["logo_content_type"] = logo_file.content_type or "image/png"
        return super().create(validated_data)
