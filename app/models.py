from django.db import models
from django.contrib.auth.hashers import make_password

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
    rarity = models.CharField(
        max_length=20,
        choices=[
            ('common', 'こもん'),
            ('rare', 'レア'),
            ('very_rare', 'げきれあ'),
            ('unusual', 'いんじゃない'),
            ('not_very_rare', 'なかなかレア'),
        ],
        default='common'
    )
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.word
