from django.db import models

# Create your models here.
class Plant(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    light = models.CharField(max_length=100, default='Medium indirect light')
    water = models.CharField(max_length=100, default='When soil is dry')
    humidity = models.CharField(max_length=100, default='Any humidity will do!')

    def __str__(self):
        return self.name