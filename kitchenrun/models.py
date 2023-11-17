from django.db import models

from main.models import Event,User


# Create your models here.

class EventProperty(models.Model):

    # attributes
    event = models.OneToOneField(Event, on_delete=models.CASCADE)
    applications_start = models.DateTimeField()
    applications_end = models.DateTimeField()
    hasAppetizer = models.BooleanField(default=True)
    hasMainCourse = models.BooleanField(default=True)
    hasDessert = models.BooleanField(default=True)
    start_time = models.TimeField()
    length_courses = models.DurationField(default='1h')
    length_breaks = models.DurationField(default='30min')
    public = models.BooleanField(default=False)
    team_size = models.SmallIntegerField(default=3)

class Team(models.Model):
    event = models.ForeignKey(EventProperty, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True)
    street = models.CharField(max_length=255, blank=True)
    number = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=255, blank=True)
    address_addition = models.TextField(blank=True)
    is_vegan = models.BooleanField(default=False)
    is_vegetarian = models.BooleanField(default=False)
    is_halal = models.BooleanField(default=False)
    is_kosher = models.BooleanField(default=False)
    allergies = models.TextField(blank=True)
    comments = models.TextField(blank=True)


class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)