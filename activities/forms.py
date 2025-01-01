from django import forms
from .models import Activity

class ActivityForm(forms.ModelForm):
    latitude = forms.FloatField(required=False, widget=forms.HiddenInput())
    longitude = forms.FloatField(required=False, widget=forms.HiddenInput())
    
    class Meta:
        model = Activity
        fields = ['blend_name', 'blend_type', 'rating', 'location', 'notes', 'latitude', 'longitude']
