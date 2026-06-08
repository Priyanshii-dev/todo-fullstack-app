# todolist/api/tasks/task_update.py
from rest_framework import permissions
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView

from todolist.serializers.tasks import TaskSerializer
from ..responses import success_response
from ...utils.task_helpers import get_single_task_for_user


class TaskUpdateAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes     = [MultiPartParser, FormParser]

    def put(self, request, task_id):
        task = get_single_task_for_user(request.user, task_id)
        serializer = TaskSerializer(task, data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return success_response(
            data=serializer.data,
            message="Task updated successfully.",
        )

    def patch(self, request, task_id):
        task = get_single_task_for_user(request.user, task_id)
        serializer = TaskSerializer(task, data=request.data, partial=True, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return success_response(
            data=serializer.data,
            message="Task updated successfully.",
        )
