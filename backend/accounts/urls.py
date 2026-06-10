from django.urls import path
from .api.login    import LoginAPI  
from .api.register import RegisterAPI
from .api.admin    import UserListAPI, UserStatusUpdateAPI
from .api.employee import EmployeeDashboardAPI
from .api.verify_otp import VerifyOTPAPI
from .api.resend_otp import ResendOTPAPI
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


path("api/auth/verify-otp/", VerifyOTPAPI.as_view(), name="api_auth_verify_otp"),
path("api/auth/resend-otp/", ResendOTPAPI.as_view(), name="api_auth_resend_otp"),

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
