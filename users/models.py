from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    city = models.CharField(max_length=100, verbose_name="Город")
    image = models.ImageField(upload_to="users/", blank=True, verbose_name="Изображение")
