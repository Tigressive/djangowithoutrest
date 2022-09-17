from django import forms
from django.core.exceptions import ValidationError

from .models import Items


class ItemsForm(forms.ModelForm):
    class Meta:
        model = Items
        fields = ('name', 'location', 'isPrivate', 'price')

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) <= 2:
            raise ValidationError('Item names must be longer than 2 characters!')
        return name


class ItemCreateForm(forms.ModelForm):
    class Meta:
        model = Items
        fields = ('name', 'isPrivate', 'price')



