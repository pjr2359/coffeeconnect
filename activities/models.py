from django.db import models
from django.conf import settings # Use settings.AUTH_USER_MODEL
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime

# Define choices for brew methods
BREW_METHODS = [
    ('aeropress', 'Aeropress'),
    ('french_press', 'French Press'),
    ('espresso', 'Espresso'),
    ('latte', 'Latte'),
    ('cappuccino', 'Cappuccino'),
    ('freddo_espresso', 'Freddo Espresso'),
    ('greek_coffee', 'Greek Coffee'),
    ('pour_over', 'Pour Over'),
    ('drip', 'Drip Machine'),
    ('moka_pot', 'Moka Pot'),
    ('cold_brew', 'Cold Brew'),
    ('other', 'Other'),
]

class GrinderSetting(models.Model):
    """Model to store user's grinder settings"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='grinders')
    grinder_name = models.CharField(max_length=100)
    min_setting = models.IntegerField(default=1)
    max_setting = models.IntegerField(default=40)
    step_size = models.DecimalField(max_digits=3, decimal_places=1, default=1)
    is_default = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username}'s {self.grinder_name}"
    
    def save(self, *args, **kwargs):
        if self.is_default:
            # Set all other grinders for this user to not default
            GrinderSetting.objects.filter(user=self.user).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)

class CoffeeLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='coffee_logs')
    coffee_name = models.CharField(max_length=100, help_text="Name of the coffee bean or blend") # Renamed from blend_name
    water_amount_ml = models.PositiveIntegerField(blank=True, null=True, help_text="Amount of water used in ml")
    bean_grams = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True, validators=[MinValueValidator(0.1)], help_text="Amount of coffee beans used in grams")
    brew_method = models.CharField(max_length=50, choices=BREW_METHODS)
    steep_time = models.DurationField(blank=True, null=True, help_text="Steeping or brewing time (e.g., 00:04:00 for 4 minutes)") # Changed to DurationField
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], help_text="Your rating from 1 to 5") # Adjusted range if needed
    notes = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    # New fields
    grind_size = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, help_text="Grind size setting on your grinder")
    grinder = models.ForeignKey(GrinderSetting, on_delete=models.SET_NULL, related_name='coffee_logs', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s {self.coffee_name} ({self.brew_method}) on {self.timestamp.strftime('%Y-%m-%d')}"

    # Optional: Add a property for steep time in seconds if needed for display
    @property
    def steep_time_seconds(self):
        if self.steep_time:
            return self.steep_time.total_seconds()
        return None
        
    @property
    def brew_ratio(self):
        """Calculate the water to coffee ratio"""
        if self.water_amount_ml and self.bean_grams and self.bean_grams > 0:
            return round(self.water_amount_ml / float(self.bean_grams), 1)
        return None