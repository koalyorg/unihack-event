from django import forms
from .models import EventProperty, Course
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class EventPropertyForm(forms.ModelForm):
    class Meta:
        model = EventProperty
        exclude = ['event']  # Excluding owner and participants
        widgets = {
            'length_courses': forms.TimeInput(format='%H'),
            'length_breaks': forms.TimeInput(format='%H'),
            'team_size': forms.NumberInput(),
            'guest_per_course': forms.NumberInput(),
            'course_number': forms.NumberInput(),
            # Define other widgets as needed
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = ['event_property', 'order']
        widgets = {
            'name': forms.TextInput(),
        }


