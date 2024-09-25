# generator/models.py
from django.db import models

class Theme(models.Model):
    text = models.CharField(max_length=255, verbose_name='テーマ')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
