from django import forms
from .models import CoffeeLog, GrinderSetting, BREW_METHODS
import datetime

class GrinderSettingForm(forms.ModelForm):
    """Form for creating and editing grinder settings"""
    class Meta:
        model = GrinderSetting
        fields = ['grinder_name', 'min_setting', 'max_setting', 'step_size', 'is_default']
        widgets = {
            'grinder_name': forms.TextInput(attrs={'class': 'form-control'}),
            'min_setting': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'max_setting': forms.NumberInput(attrs={'class': 'form-control', 'min': '2'}),
            'step_size': forms.NumberInput(attrs={'class': 'form-control', 'min': '0.1', 'step': '0.1'})
        }

class CoffeeLogForm(forms.ModelForm):
    # Use a CharField with a widget for DurationField if direct input is desired
    steep_time_input = forms.CharField(
        required=False,
        help_text="Enter steep time (e.g., MM:SS or H:MM:SS)",
        label="Steep Time"
    )

    class Meta:
        model = CoffeeLog
        fields = [
            'coffee_name', 
            'water_amount_ml', 
            'bean_grams', 
            'brew_method',
            'steep_time_input',
            'rating', 
            'notes',
            'grinder',
            'grind_size'
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
            'grinder': forms.Select(attrs={'class': 'form-control'}),
            'grind_size': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Limit grinder choices to the user's grinders if user is provided
        if user:
            self.fields['grinder'].queryset = GrinderSetting.objects.filter(user=user)
            
            # If user has no grinders, hide the grinder field
            if not self.fields['grinder'].queryset.exists():
                self.fields['grinder'].widget = forms.HiddenInput()
                self.fields['grind_size'].help_text = "Add a grinder in your profile to track settings"

    def clean_steep_time_input(self):
        data = self.cleaned_data['steep_time_input']
        if not data:
            return None # Allow empty input
        
        parts = data.split(':')
        try:
            if len(parts) == 2: # MM:SS
                minutes = int(parts[0])
                seconds = int(parts[1])
                if not (0 <= minutes < 60 and 0 <= seconds < 60):
                    raise ValueError("Invalid time format.")
                return datetime.timedelta(minutes=minutes, seconds=seconds)
            elif len(parts) == 3: # H:MM:SS
                hours = int(parts[0])
                minutes = int(parts[1])
                seconds = int(parts[2])
                if not (0 <= hours < 24 and 0 <= minutes < 60 and 0 <= seconds < 60):
                    raise ValueError("Invalid time format.")
                return datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
            else:
                raise ValueError("Invalid time format. Use MM:SS or H:MM:SS.")
        except ValueError:
            raise forms.ValidationError("Invalid time format. Use MM:SS or H:MM:SS.")

    def save(self, commit=True):
        # Get the cleaned duration from the input field
        self.instance.steep_time = self.cleaned_data.get('steep_time_input')
        return super().save(commit=commit)
