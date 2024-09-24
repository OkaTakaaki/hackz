from django import forms
from .models import Goal

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['objective', 'motivation', 'achievement', 'turned']

        # 各フィールドのウィジェットを指定
        widgets = {
            'motivation': forms.NumberInput(
                attrs={
                    'type': 'range',   # スライダーにするため
                    'min': '0',        # 最小値
                    'max': '10',       # 最大値
                    'step': '1',       # 1刻みで調整
                    'class': 'slider'  # スライダー用のクラス
                }
            ),
            'achievement': forms.NumberInput(
                attrs={
                    'type': 'range',
                    'min': '0',
                    'max': '10',
                    'step': '1',
                    'class': 'slider'
                }
            )
        }