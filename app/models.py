from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
     created_at = models.DateField(verbose_name="登録日時", auto_now_add=True)
