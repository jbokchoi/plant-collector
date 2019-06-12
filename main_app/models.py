from django.db import models
from django.urls import reverse
from datetime import date

MEALS = (
  ('W', 'Water'),
  ('L', 'Light'),
  ('F', 'Fertilizer')
)

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
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'plant_id': self.id})

    def fed_for_today(self):
        return self.feeding_set.filter(date=date.today()).count() >= len(MEALS)

class Feeding(models.Model):
    date = models.DateField('feeding date')
    meal = models.CharField(
        max_length=1,
        choices=MEALS,
        default=MEALS[0][0]
    )
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_meal_display()} on {self.date}"

    class Meta:
        ordering = ['-date']