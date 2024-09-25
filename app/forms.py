# generator/forms.py
from django import forms
from .models import Theme

class ThemeForm(forms.ModelForm):
    class Meta:
        model = Theme
        fields = ['text']
        labels = {
            'text': 'モチベーションを高めたいテーマを入力してください',
        }
