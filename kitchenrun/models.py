from django.db import models

import uuid

from main.models import Event,User

import uuid


# Create your models here.

class EventProperty(models.Model):
    # attributes
    event = models.OneToOneField(Event, on_delete=models.CASCADE)
    #applications_start = models.DateTimeField()
    #applications_end = models.DateTimeField()
    #hasAppetizer = models.BooleanField(default=True)
    #hasMainCourse = models.BooleanField(default=True)
    #hasDessert = models.BooleanField(default=True)
    #start_time = models.TimeField()
    length_courses = models.DurationField(default='01:00:00')
    length_breaks = models.DurationField(default='00:30:00')
    #team_size = models.SmallIntegerField(default=3)
    #guests_per_course = models.SmallIntegerField(default=2)
    #course_number = models.SmallIntegerField(default=3)


class Team(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    number = models.CharField(max_length=10)
    city = models.CharField(max_length=255)
    address_addition = models.CharField(max_length=255, blank=True)
    lat = models.DecimalField(default=-1, decimal_places=7, max_digits=10)
    lon = models.DecimalField(default=-1, decimal_places=7, max_digits=10)
    is_vegan = models.BooleanField(default=False)
    is_vegetarian = models.BooleanField(default=False)
    is_halal = models.BooleanField(default=False)
    is_kosher = models.BooleanField(default=False)
    allergies = models.TextField(blank=True)
    comments = models.TextField(blank=True)
    team_member_1 = models.CharField(max_length=255)
    team_member_2 = models.CharField(max_length=255)


# class TeamMember(models.Model):
#     team = models.ForeignKey(Team, on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)

# class Course(models.Model):
#     event_property = models.ForeignKey(EventProperty, on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     order = models.SmallIntegerField(default=0)

class Pair(models.Model):
    COURSE_TYPES = [
        (0, 'Appetizer'),
        (1, 'Main Dish'),
        (2, 'Dessert'),
    ]
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    course = models.SmallIntegerField(
        choices=COURSE_TYPES,
        default=0,
    )
    #course = models.ForeignKey(Course, on_delete=models.CASCADE)
    cook = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="cook_id")
    guest_1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="guest_1_id")
    guest_2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="guest_2_id")
    #pair_id = models.UUIDField(default=uuid.uuid4)