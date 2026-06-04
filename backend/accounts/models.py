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
        extra.setdefault('is_staff', True)
        extra.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra)


class User(AbstractUser):
    username = None
    email    = models.EmailField(unique=True)

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Role(models.TextChoices):
        ADMIN    = 'admin',    'Admin'
        HR       = 'hr',       'HR'
        EMPLOYEE = 'employee', 'Employee'

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.EMPLOYEE)

    def __str__(self):
        return self.email