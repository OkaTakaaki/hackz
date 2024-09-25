from django import forms
from .models import Aphorism
from .models import Collection

class AdminLoginForm(forms.Form):
    adminname = forms.CharField(label="Admin Name", max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

class AphorismForm(forms.ModelForm):
    class Meta:
        model = Aphorism
        fields = ['word', 'author', 'picture', 'rarity']

class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['word', 'author', 'picture', 'acquision_date']
