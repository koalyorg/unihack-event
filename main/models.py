from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_user_property(sender, instance, created, **kwargs):
    if created:
        UserProperty.objects.create(user=instance)

class UserProperty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Event(models.Model):

    EVENT_TYPES = [
        ('CONCERT', 'Concert'),
        ('CONFERENCE', 'Conference'),
        ('WORKSHOP', 'Workshop'),
        ('MEETUP', 'Meetup'),
        ('KITCHENRUN', 'Kitchenrun'),
        ('Hackathon', 'Hackathon'),
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
    timezone = models.CharField(max_length=50)  # e.g., 'Europe/London'
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    organizer = models.CharField(max_length=100, blank=True)
    max_participants = models.PositiveIntegerField(null=True, blank=True)
    is_virtual = models.BooleanField(default=False)
    url = models.URLField(blank=True)

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
    def participant_count(self):
        return self.participants.count()

    def can_add_participant(self):
        if self.max_participants is not None:
            return self.participant_count < self.max_participants
        return True

    class Meta:
        ordering = ['start_time']
