from typing import Optional, TypeVar

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from common.models import BaseModel

UserType = TypeVar("UserType", bound=AbstractUser)


class UserManager(BaseUserManager):
    def create_user(self, username: str, email: str, password: Optional[str] = None, **extra_fields) -> UserType:
        """
        Create a new user method

        Parameters
        ----------
        username : str
            Creating user username
        email : str
            Creating user email
        password : str, optional
            Creating user password
        **extra_fields : dict
            Create user extra fields

        Returns
        -------
        _ : UserType
            AbstractUser's subclass class instance
        """
        if username is None:
            raise TypeError("username must not be None")
        if email is None:
            raise TypeError("email must not be None")

        user = self.model(username=username, email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username: str, email: str, password: str, **extra_fields) -> UserType:
        """
        Create a superuser

        Parameters
        ----------
        username : str
            Creating user username
        email : str
            Creating user email
        password : str, optional
            Creating user password
        **extra_fields :
            Create user extra fields

        Returns
        -------
        _ : UserType
            AbstractUser's subclass class instance with superuser permissions
        """
        if password is None:
            raise TypeError("password must not be None")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff = True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser = True")

        return self.create_user(username, email, password, **extra_fields)


class User(BaseModel, AbstractUser):
    username = models.CharField(max_length=255, db_index=True, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self) -> str:
        return f"{self.username}({self.email})"
