from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
     created_at = models.DateField(verbose_name="登録日時", auto_now_add=True)

class Collection(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # userid = models.IntegerField()
    word = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    picture = models.ImageField(upload_to='images/')
    acquision_date = models.DateTimeField("Acquisition date")
    rarity = models.CharField(
        max_length=20,
        choices=[
            ('こもん', 'common'),
            ('れあ', 'rare'),
            ('げきれあ', 'very_rare'),
            ('いいんじゃない', 'unusual'),
            ('なかなかレア', 'not_very_rare'),
        ],
        default='common'
    )