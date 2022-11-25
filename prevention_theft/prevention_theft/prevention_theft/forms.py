from django import forms
from .models import Item
class RegistItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["name"]

        labels = {
            "name": "이름",
        }