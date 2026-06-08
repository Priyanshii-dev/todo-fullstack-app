# todolist/api/tasks/task_create.py
from rest_framework import permissions
from rest_framework.parsers import FormParser, MultiPartParser,JSONParser
from rest_framework.views import APIView

from todolist.serializers.tasks import TaskSerializer
from ..responses import success_response
from todolist.utils.cache import clear_user_tasks_cache


class TaskCreateAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes     = [ JSONParser, MultiPartParser, FormParser]

    def post(self, request):
        serializer = TaskSerializer(
            data=request.data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        # Clear Redis cache
        clear_user_tasks_cache(request.user.id)

        return success_response(
            data=serializer.data,
            message="Task created successfully.",
            status_code=201,
        )
