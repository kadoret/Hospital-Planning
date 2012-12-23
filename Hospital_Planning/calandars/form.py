from django import forms
from models import Calandars

class CalandarsForm(forms.ModelForm):
    class Meta:
        model =  Calandars
