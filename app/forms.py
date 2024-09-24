from django import forms
from .models import Schedule
from django import forms
from .models import Goal


class BS4ScheduleForm(forms.ModelForm):
    """Bootstrapに対応するためのModelForm"""

    class Meta:
        model = Schedule
        fields = ('summary', 'description', 'start_time', 'end_time')
        widgets = {
            'summary': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
            }),
            'start_time': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'end_time': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }

    def clean_end_time(self):
        start_time = self.cleaned_data['start_time']
        end_time = self.cleaned_data['end_time']
        if end_time <= start_time:
            raise forms.ValidationError(
                '終了時間は、開始時間よりも後にしてください'
            )
        return end_time

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