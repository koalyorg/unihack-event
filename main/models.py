from django.db import models

import pycountry

# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone



@receiver(post_save, sender=User)
def create_user_property(sender, instance, created, **kwargs):
    if created:
        UserProperty.objects.create(user=instance)


class UserProperty(models.Model):

    COUNTRIES = [None] * len(pycountry.countries)
    i = 0
    for country in list(pycountry.countries):
        COUNTRIES[i] = (country.alpha_3, country.name)
        i=i+1

    # attributes
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    street = models.CharField(max_length=255, blank=True)
    number = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=255, blank=True)
    country = models.CharField(
        max_length=10,
        choices=COUNTRIES,
        default='DEU')


class Event(models.Model):
    EVENT_TYPES = [
        ('CONCERT', 'Concert'),
        ('CONFERENCE', 'Conference'),
        ('WORKSHOP', 'Workshop'),
        ('MEETUP', 'Meetup'),
        ('KITCHENRUN', 'Kitchenrun'),
        ('HACKATHON', 'Hackathon'),
        ('OTHER', 'Other'),
    ]

    # Attributes
    title = models.CharField(max_length=200)
    event_type = models.CharField(
        max_length=10,
        choices=EVENT_TYPES,
        default='OTHER',
    )
    start_time = models.DateTimeField()
    duration = models.DurationField()  # stores a timedelta object
    registration_end = models.DateTimeField()
    timezone = models.CharField(max_length=50)  # e.g., 'Europe/London'
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    organizer = models.CharField(max_length=100, blank=True)
    max_participants = models.PositiveIntegerField(null=True, blank=True)
    lat = models.FloatField(verbose_name="Latitude", null=True)
    long = models.FloatField(verbose_name="Longitude", null=True)
    is_virtual = models.BooleanField(default=False)
    url = models.URLField(blank=True)
    lat = models.DecimalField(default=-1, decimal_places=7, max_digits=10)
    lon = models.DecimalField(default=-1, decimal_places=7, max_digits=10)

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='events',
    )

    # New field for event participants
    participants = models.ManyToManyField(
        User,
        related_name='participating_events',
        blank=True
    )

    def __str__(self):
        return f"{self.title} ({self.get_event_type_display()})"

    @property
    def end_time(self):
        return self.start_time + self.duration

    @property
    def registration_open(self):
        if self.registration_end > timezone.now():
            return True
        else:
            return False

    @property
    def status(self):
       if self.registration_open:
           if self.can_add_participant():
               return "Registration open"
           else:
               return "Full"
       else:
            if self.start_time > timezone.now():
                return "Registration closed"
            if self.start_time + self.duration < timezone.now():
                return "Event finished"
            else:
                return "Event running"

    @property
    def participant_count(self):
        return self.participants.count()

    def participant_limit_reached(self):
        if self.max_participants is not None:
            return not self.participant_count < self.max_participants
        return False

    def can_add_participant(self):
        if not self.participant_limit_reached() and self.registration_open:
            return True
        else:
            return False

    class Meta:
        ordering = ['start_time']
