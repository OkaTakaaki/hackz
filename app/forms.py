from django import forms
from .models import Aphorism

class AdminLoginForm(forms.Form):
    adminname = forms.CharField(label="Admin Name", max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, label="Password")




class AphorismForm(forms.ModelForm):
    class Meta:
        model = Aphorism
        fields = ['word', 'author', 'picture', 'rarity']

