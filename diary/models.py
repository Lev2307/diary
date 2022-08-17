from django.db import models
from django.contrib.auth.models import User

# Create your models here
class DiaryModel(models.Model):
    class ChooseDayOfTheWeek(models.TextChoices):
        MONDAY = 'monday'
        Tuesday = 'tuesday'
        WEDNESDAY = 'wednesday'
        THURSDAY = 'thursday'
        FRIDAY = 'friday'
        SATURDAY = 'saturday'
        SUNDAY = 'sunday'
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    header = models.CharField(max_length=65, default='')
    text = models.TextField()
    day_of_the_week = models.CharField(
        max_length=15,
        choices=ChooseDayOfTheWeek.choices,
        default='',
    )
    date = models.DateTimeField(auto_now_add=True)