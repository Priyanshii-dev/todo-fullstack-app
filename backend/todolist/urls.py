from django.urls import path

from .api.tasks.task_create import TaskCreateAPI
from .api.tasks.task_delete import TaskDeleteAPI
from .api.tasks.task_detail import TaskDetailAPI
from .api.tasks.task_fetch import TaskListAPI
from .api.tasks.task_filter import TaskStatusFilterAPI
from .api.tasks.task_logo import TaskLogo
from .api.tasks.task_logo_serve import TaskLogoServeAPI
from .api.tasks.task_search import TaskSearchAPI
from .api.tasks.task_toggle import TaskToggleAPI
from .api.tasks.task_update import TaskUpdateAPI

urlpatterns = [

    # TASKS
    path(
        "api/tasks/",
        TaskListAPI.as_view(),
        name="api_tasks"
    ),

    path(
        "api/tasks/create/",
        TaskCreateAPI.as_view(),
        name="api_task_create"
    ),

    path(
        "api/tasks/search/",
        TaskSearchAPI.as_view(),
        name="api_task_search"
    ),

    path(
        "api/tasks/filter/",
        TaskStatusFilterAPI.as_view(),
        name="api_task_filter"
    ),

    path(
        "api/tasks/<int:task_id>/",
        TaskDetailAPI.as_view(),
        name="api_task_detail"
    ),

    path(
        "api/tasks/edit/<int:task_id>",
        TaskUpdateAPI.as_view(),
        name="api_task_update"
    ),

    path(
        "api/tasks/delete/<int:task_id>",
        TaskDeleteAPI.as_view(),
        name="api_task_delete"
    ),

    path(
        "api/tasks/toggle/<int:task_id>",
        TaskToggleAPI.as_view(),
        name="api_task_toggle"
    ),

    path(
        "api/tasks/<int:task_id>/logo/",
        TaskLogoServeAPI.as_view(),
        name="api_task_logo_serve"
    ),
]
