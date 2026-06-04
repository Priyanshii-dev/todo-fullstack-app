from django.urls import path
from .api.login    import LoginAPI  
from .api.register import RegisterAPI
from .api.admin    import UserListAPI, UserStatusUpdateAPI
from .api.employee import EmployeeDashboardAPI

urlpatterns = [
    # Auth (public)
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

    # Employee
    path(
        "api/employee/dashboard/", 
        EmployeeDashboardAPI.as_view(), 
        name="api_employee_dashboard"
    ),

    # Admin
    path(
        "api/admin/users/",         
        UserListAPI.as_view(),          
        name="api_admin_user_list"
    ),
    path(
        "api/admin/users/<int:pk>/", 
        UserStatusUpdateAPI.as_view(), 
        name="api_admin_user_update"
    ),
]
