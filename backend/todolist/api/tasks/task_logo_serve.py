from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from todolist.models import Task


class TaskLogoServeAPI(APIView):
    """
    GET /api/tasks/<task_id>/logo/
    Reads raw binary logo from the DB and serves it as an image response.
    Public (AllowAny) so it works directly in <img src> tags without auth headers.
    """
    permission_classes = [AllowAny]

    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)

        if not task.logo:
            return HttpResponse(status=404)

        return HttpResponse(
            bytes(task.logo),
            content_type=task.logo_content_type or "image/png",
        )
