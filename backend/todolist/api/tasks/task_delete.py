from rest_framework import permissions
from rest_framework.views import APIView

from todolist.serializers.tasks import TaskSerializer
from ..responses import success_response
from ...utils.task_helpers import get_single_task_for_user
from todolist.utils.cache import clear_user_tasks_cache


class TaskDeleteAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, task_id):
        task = get_single_task_for_user(request.user, task_id)

        # Serialize before deleting so the response includes full task data + logo
        serializer = TaskSerializer(task, context={"request": request})
        data = serializer.data

        task.delete()

        clear_user_tasks_cache(request.user.id)

        return success_response(
            data=data,
            message="Task deleted successfully.",
        )
