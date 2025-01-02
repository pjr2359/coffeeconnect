from django.db import models
from users.models import CustomUser

class Activity(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    blend_name = models.CharField(max_length=100, blank=True, null=True)
    blend_type = models.CharField(max_length=50, choices=[
        ('arabica', 'Arabica'),
        ('robusta', 'Robusta'),
        ('blend', 'Blend')
    ])
    rating = models.IntegerField()
    location = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)