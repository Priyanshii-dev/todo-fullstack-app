from rest_framework import permissions
from rest_framework.views import APIView

from todolist.serializers.tasks import TaskSerializer
from ..responses import get_positive_int, success_response
from ...utils.task_helpers import get_all_tasks_for_user
from django.core.cache import cache
from todolist.utils.cache import get_user_tasks_cache_key

def get_task_table_response(request, params):
    page = get_positive_int(params.get("page"), 1)
    limit = get_positive_int(params.get("limit"), 10)
    search = params.get("search", "").strip()
    status = params.get("status", "all")

    all_tasks = get_all_tasks_for_user(request.user)
    tasks = all_tasks

    if search:
        tasks = tasks.filter(task__icontains=search)

    if status == "completed":
        tasks = tasks.filter(is_completed=True)
    elif status == "pending":
        tasks = tasks.filter(is_completed=False)

    total = tasks.count()
    total_pages = max(1, (total + limit - 1) // limit)
    completed_total = all_tasks.filter(is_completed=True).count()

    if page > total_pages:
        page = total_pages

    start = (page - 1) * limit
    end = start + limit

    serializer = TaskSerializer(tasks[start:end], many=True, context={"request": request})

    return success_response(
        data={
            "results": serializer.data,
            "page": page,
            "limit": limit,
            "total": total,
            "totalPages": total_pages,
            "totalTasks": all_tasks.count(),
            "completedTasks": completed_total,
        },
        message="Tasks fetched successfully.",
    )


class TaskListAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        cache_key = get_user_tasks_cache_key(request.user.id)
        print("CACHE KEY:", cache_key)

        cached_data = cache.get(cache_key)

        if cached_data:
            print("FROM REDIS")
            return success_response(data=cached_data)

        print("FROM DATABASE")

        tasks = get_all_tasks_for_user(request.user)

        serializer = TaskSerializer(
            tasks,
            many=True,
            context={"request": request},
        )

        cache.set(
            cache_key,
            serializer.data,
            timeout=300,
        )

        return success_response(data=serializer.data)