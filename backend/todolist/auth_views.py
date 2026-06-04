from django.contrib import messages
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.mixins import LoginRequiredMixin
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

LOGIN_URL = "login"
TODOLIST_URL = "todolist"
REGISTER_URL = "register"


class EmailBackend(ModelBackend):
    """Authenticate using email instead of username."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        email = kwargs.get("email", username)
        if email is None or password is None:
            return None
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None


class RegisterView(View):

    template_name = "register.html"

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            return redirect(TODOLIST_URL)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):

        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")

        if not email or not password:

            messages.error(
                request,
                "Email and password are required."
            )

            return redirect(REGISTER_URL)

        if User.objects.filter(email__iexact=email).exists():

            messages.error(
                request,
                "Email already registered."
            )

            return redirect(REGISTER_URL)

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
        )

        login(request, user, backend="todolist.auth_views.EmailBackend")

        messages.success(
            request,
            "Account created successfully."
        )

        return redirect(TODOLIST_URL)


class LoginUserView(View):

    template_name = "login.html"

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            return redirect(TODOLIST_URL)

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):

        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")

        if not email or not password:

            messages.error(
                request,
                "Email and password are required."
            )

            return redirect(LOGIN_URL)

        user = authenticate(
            request,
            email=email,
            password=password,
        )

        if user is None:

            messages.error(
                request,
                "Invalid email or password."
            )

            return redirect(LOGIN_URL)
        login(request, user, backend="todolist.auth_views.EmailBackend")
        return redirect(TODOLIST_URL)


class LogoutUserView(LoginRequiredMixin, View):

    login_url = reverse_lazy(LOGIN_URL)
    http_method_names = ["post"]
    def post(self, request):
        logout(request)
        return redirect(LOGIN_URL)