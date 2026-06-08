from rest_framework import permissions
from rest_framework.views import APIView

from todolist.serializers.tasks import TaskSerializer
from ..responses import success_response
from ...utils.task_helpers import get_single_task_for_user


class TaskDetailAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, task_id):
        task = get_single_task_for_user(request.user, task_id)
        serializer = TaskSerializer(task, context={"request": request})
        return success_response(data=serializer.data)
