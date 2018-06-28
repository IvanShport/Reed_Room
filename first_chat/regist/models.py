from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.conf import settings
import os


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    activation_key = models.CharField(max_length=255, default=1)
    email_validated = models.BooleanField(default=False)

    avatar = models.ImageField(upload_to='avatar/%Y/%m/%d', default='/img/user-png-icon-male-user-icon-512.png', blank=True, null=True)

    def __str__(self):
        return self.user.username
