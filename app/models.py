from django.db import models
from django.contrib.auth.hashers import make_password
from django.db import models
from PIL import Image, ImageDraw
import os


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
