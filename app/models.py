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