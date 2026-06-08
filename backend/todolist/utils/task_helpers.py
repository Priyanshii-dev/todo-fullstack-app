from django.shortcuts import get_object_or_404

from todolist.models import Task


def get_all_tasks_for_user(user):
    return Task.objects.select_related("user").filter(
        user=user,
    ).order_by("-id")


def get_single_task_for_user(user, task_id):
    return get_object_or_404(
        Task.objects.select_related("user"),
        id=task_id,
        user=user,
    )
