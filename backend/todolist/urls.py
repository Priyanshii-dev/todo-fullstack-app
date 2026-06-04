from django.urls import path
from .api.tasks.task_logo import TaskLogo
from .api.tasks.task_logo_serve import TaskLogoServeAPI

from .api.auth.login import LoginAPI
from .api.auth.register import RegisterAPI
from .api.tasks.task_create import TaskCreateAPI
from .api.tasks.task_delete import TaskDeleteAPI
from .api.tasks.task_detail import TaskDetailAPI
from .api.tasks.task_fetch import TaskListAPI
from .api.tasks.task_filter import TaskStatusFilterAPI
from .api.tasks.task_search import TaskSearchAPI
from .api.tasks.task_toggle import TaskToggleAPI
from .api.tasks.task_update import TaskUpdateAPI
from .auth_views import LoginUserView,LogoutUserView,RegisterView

from .views import AboutView,ContactView,DeleteTaskView,HomePageView,TodoListView,ToggleTaskView   

urlpatterns = [

    # AUTH
    path(
        "register/",
        RegisterView.as_view(),
        name="register"
    ),

    path(
        "login/",
        LoginUserView.as_view(),
        name="login"
    ),

    path(
        "logout/",
        LogoutUserView.as_view(),
        name="logout"
    ),

    # HOME + PAGES
    path(
        "",
        HomePageView.as_view(),
        name="home"
    ),

    path(
        "about/",
        AboutView.as_view(),
        name="about"
    ),

    path(
        "contact/",
        ContactView.as_view(),
        name="contact"
    ),

    # TEMPLATE VIEWS
    path(
        "todolist/",
        TodoListView.as_view(),
        name="todolist"
    ),

    path(
        "todolist/<int:task_id>/toggle/",
        ToggleTaskView.as_view(),
        name="toggle_task"
    ),

    path(
        "todolist/<int:task_id>/delete/",
        DeleteTaskView.as_view(),
        name="delete_task"
    ),

    # API
    path(
        "api/auth/register/",
        RegisterAPI.as_view(),
        name="api_auth_register"
    ),

    path(
        "api/auth/login/",
        LoginAPI.as_view(),
        name="api_auth_login"
    ),

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
