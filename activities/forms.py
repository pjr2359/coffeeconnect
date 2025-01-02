from django import forms
from .models import Activity

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['blend_name', 'blend_type', 'rating', 'location', 'notes', 'latitude', 'longitude']
