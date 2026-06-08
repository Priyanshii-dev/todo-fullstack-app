from rest_framework import permissions
from rest_framework.views import APIView

from todolist.serializers.tasks import TaskSerializer
from ..responses import success_response
from ...utils.task_helpers import get_single_task_for_user
from todolist.utils.cache import clear_user_tasks_cache


class TaskToggleAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, task_id):
        task = get_single_task_for_user(request.user, task_id)
        task.is_completed = not task.is_completed
        task.save(update_fields=["is_completed"])

        clear_user_tasks_cache(request.user.id)

        serializer = TaskSerializer(task, context={"request": request})

        return success_response(
            data=serializer.data,
            message="Task toggled successfully.",
        )
