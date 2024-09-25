from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from PIL import Image, ImageDraw
import os
import datetime

class Schedule(models.Model):
    """スケジュール"""
    summary = models.CharField('概要', max_length=50)
    description = models.TextField('詳細な説明', blank=True)
    start_time = models.TimeField('開始時間', default=datetime.time(7, 0, 0))
    end_time = models.TimeField('終了時間', default=datetime.time(7, 0, 0))
    date = models.DateField('日付')
    created_at = models.DateTimeField('作成日', default=timezone.now)


class CustomUser(AbstractUser):
     created_at = models.DateField(verbose_name="登録日時", auto_now_add=True)

class Collection(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # userid = models.IntegerField()
    word = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    picture = models.ImageField(upload_to='images/')
    acquision_date = models.DateTimeField("Acquisition dat")
    rarity = models.IntegerField(
        max_length=20,
        choices=[
            (1, '☆'),
            (2, '☆☆'),
            (3, '☆☆☆'),
            (4, '☆☆☆☆'),
            (5, '☆☆☆☆☆'),
        ],
    )

class AdminUser(models.Model):
    adminname = models.CharField(max_length=100)
    password = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
        # パスワードをハッシュ化して保存
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

class Aphorism(models.Model):
    word = models.CharField(max_length=100)
    author = models.CharField(max_length=100, blank=True, null=True)
    picture = models.ImageField(upload_to='images/')  
    rarity = models.IntegerField(
        max_length=20,
        choices=[
            (1, '☆'),
            (2, '☆☆'),
            (3, '☆☆☆'),
            (4, '☆☆☆☆'),
            (5, '☆☆☆☆☆'),
        ],
        default='common'
    )
    created_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # まず画像を保存

        # 画像のパスを取得
        image_path = self.picture.path
        # 画像を丸く加工
        self.make_circle_image(image_path)

    def make_circle_image(self, image_path):
        # 画像を開く
        img = Image.open(image_path).convert("RGBA")

        # 正方形のサイズを決める
        size = min(img.size)
        mask = Image.new('L', (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)

        # 画像を中央に合わせてトリミング
        img = img.crop(((img.width - size) // 2, (img.height - size) // 2,
                        (img.width + size) // 2, (img.height + size) // 2))

        # 円形マスクを適用
        img.putalpha(mask)

        # PNGとして保存
        img.save(image_path, format="PNG")

    def __str__(self):
        return self.summary

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
        validators=[MinValueValidator(0), MaxValueValidator(100)],  # 0から100の範囲に制限
        blank=True,  # フォームで空欄を許可
        null=True    # データベースでnullを許可
    )
    number = models.IntegerField(verbose_name="件数", blank=True, null=True)
    turned = models.CharField(verbose_name="振り返り", max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(verbose_name="作成日")


    def __str__(self):
        return f"{self.objective} ({self.achievement}%)"