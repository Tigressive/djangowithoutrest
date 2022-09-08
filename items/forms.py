from django import forms
from django.core.exceptions import ValidationError

from .models import Items


class ItemsForm(forms.ModelForm):
    class Meta:
        model = Items
        fields = ('name', 'location')

    def clean_name(self):
        name = self.cleaned_data['name']
        if 'Django' not in name:
            raise ValidationError('We only accept items about Django')
        return name
