from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from .managers import CustomUserManager



class Sms(models.Model):
    phone = models.CharField(max_length=11)
    sms = models.CharField(max_length=6)

    class Meta:
        verbose_name = ('Sm')

    def __str__(self):
        return f'{self.phone} ---- {self.sms}'


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(
        max_length=40, blank=True, null=True)
    last_name = models.CharField(
        max_length=40, blank=True, null=True)
    phone = models.CharField(
        max_length=11, unique=True, blank=False, null=False)
    password = models.CharField(max_length=200)


    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verifed = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = ('User')

    def __str__(self):
        return f"{self.first_name}  ---  {self.phone}"
