from rest_framework import permissions
from rest_framework.views import APIView

from todolist.serializers.tasks import TaskSerializer
from ..responses import success_response
from ...utils.task_helpers import get_all_tasks_for_user


class TaskSearchAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        name = request.data.get("name", "").strip()
        tasks = get_all_tasks_for_user(request.user)

        if name:
            tasks = tasks.filter(task__icontains=name)

        serializer = TaskSerializer(tasks, many=True, context={"request": request})

        return success_response(
            data=serializer.data,
            message="Tasks searched successfully.",
        )
