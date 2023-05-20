from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from .managers import CustomUserManager



class Sms(models.Model):
    phone = models.CharField(max_length=11)
    sms = models.CharField(max_length=6)
    sentDate = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = ('Sm')

    def __str__(self):
        return f'{self.phone} ---- {self.sms}'


class User(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(
        max_length=40, blank=True, null=True)
    phone = models.CharField(
        max_length=11, unique=True, blank=False, null=False)
    password = models.CharField(max_length=200)


    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = ('User')

    def __str__(self):
        return f"{self.full_name}  ---  {self.phone}"




class Salon(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    # Other salon attributes like opening hours, facilities, etc.



class Court(models.Model):
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='courts')
    name = models.CharField(max_length=100)
    # Other court attributes like size, surface type, etc.





class Reservation(models.Model):
    court = models.ForeignKey(Court, on_delete=models.CASCADE, related_name='reservations')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    # Other reservation attributes like payment status, duration, etc.
