from rest_framework import permissions
from rest_framework.views import APIView

from todolist.serializers.tasks import TaskSerializer
from ..responses import success_response
from ...utils.task_helpers import get_all_tasks_for_user


class TaskStatusFilterAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        is_completed = request.data.get("is_completed")
        tasks = get_all_tasks_for_user(request.user)

        if isinstance(is_completed, bool):
            tasks = tasks.filter(is_completed=is_completed)

        serializer = TaskSerializer(tasks, many=True, context={"request": request})

        return success_response(
            data=serializer.data,
            message="Tasks filtered successfully.",
        )
