from django import forms
from . import models

class CreateTTB(forms.ModelForm):
    class Meta:
        model = models.TTB
        fields = [
            'image',
            'brand',
            'alcohol_type',
            'abv',
            'volume',
            'v_units',
            'origin',
            'age',
            'bottler',
            'bottler_address',
            'health_warnings',
        ]
        widgets = {
            'origin': forms.TextInput(attrs={
                'placeholder': "Input 'USA' unless imported",
            }),
        }