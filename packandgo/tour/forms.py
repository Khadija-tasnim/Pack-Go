from django import forms
from .models import TourDestinations, TourImage

class TourDestinationForm(forms.ModelForm):
    class Meta:
        model = TourDestinations
        fields = ['name', 'description', 'price_per_day']

class TourImageForm(forms.ModelForm):
    class Meta:
        model = TourImage
        fields = ['tour', 'image']
