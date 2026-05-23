from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _


# Create your models here.


class UserManager(BaseUserManager):
    """
    Custom user model manager where username is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError(_('Error: The User you want to create must have an username, try again'))
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True"))

        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User Model for our app
    """

    username = models.CharField(verbose_name='username',max_length=50, unique=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    position = models.ForeignKey("Position",on_delete=models.SET_NULL,null=True,blank=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __str__(self):
        return self.username
    

class Position(models.Model):
    """class for user position query"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name