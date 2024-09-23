from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

class CustomUser(AbstractUser):
     created_at = models.DateField(verbose_name="登録日時", auto_now_add=True)

class Goal(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    objective = models.CharField(verbose_name="目標", max_length=100)
    achievement = models.IntegerField(
        verbose_name="達成度", 
        validators=[MinValueValidator(0), MaxValueValidator(100)]  # 0 から 100 の範囲に制限
    )
    turned = models.CharField(verbose_name="振り返り", max_length=200)
    created_at = models.DateField(verbose_name="作成日", auto_now_add=True)

    def __str__(self):
        return f"{self.objective} ({self.achievement}%)"