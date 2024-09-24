import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator


class Schedule(models.Model):
    """スケジュール"""
    summary = models.CharField('概要', max_length=50)
    description = models.TextField('詳細な説明', blank=True)
    start_time = models.TimeField('開始時間', default=datetime.time(7, 0, 0))
    end_time = models.TimeField('終了時間', default=datetime.time(7, 0, 0))
    date = models.DateField('日付')
    created_at = models.DateTimeField('作成日', default=timezone.now)

    def __str__(self):
        return self.summary

class CustomUser(AbstractUser):
     created_at = models.DateField(verbose_name="登録日", auto_now_add=True)

class Goal(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    motivation = models.IntegerField(
        verbose_name="モチベーション", 
        validators=[MinValueValidator(0), MaxValueValidator(10)],  # 0から10の範囲に制限
        blank=True,  # フォームで空欄を許可
        null=True    # データベースでnullを許可
    )
    objective = models.CharField(verbose_name="目標", max_length=100)
    achievement = models.IntegerField(
        verbose_name="達成度", 
        validators=[MinValueValidator(0), MaxValueValidator(10)],  # 0から10の範囲に制限
        blank=True,  # フォームで空欄を許可
        null=True    # データベースでnullを許可
    )
    turned = models.CharField(verbose_name="振り返り", max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(verbose_name="作成日", auto_now_add=True)


    def __str__(self):
        return f"{self.objective} ({self.achievement}%)"