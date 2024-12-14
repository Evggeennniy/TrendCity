from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    phone_code = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Користувач'
        verbose_name_plural = 'Користувачi'
