from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user  = self.model(email=email, **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra):
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)
        # extra.setdefault("role", User.Role.ADMIN)
        # extra.setdefault("status", User.Status.APPROVED)
        extra.setdefault("role", "admin")       # ← use string literals
        extra.setdefault("status", "approved")

        return self.create_user(email, password, **extra)


class User(AbstractUser):
    username = None
    email    = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        EMPLOYEE = "employee", "Employee"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.EMPLOYEE,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.email