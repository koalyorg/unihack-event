from django import forms
from .models import EventProperty
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class EventPropertyForm(forms.ModelForm):
    class Meta:
        model = EventProperty
        exclude = ['event']  # Excluding owner and participants
        widgets = {
            'length_courses': forms.TextInput(attrs={'placeholder': 'HH:MM:SS'}),
            'length_breaks': forms.TextInput(attrs={'placeholder': 'HH:MM:SS'}),
            'team_size': forms.NumberInput(),
            'guest_per_course': forms.NumberInput(),
            'course_number': forms.NumberInput(),
            # Define other widgets as needed
        }
#
# class CourseForm(forms.ModelForm):
#     class Meta:
#         model = Course
#         exclude = ['event_property', 'order']
#         widgets = {
#             'name': forms.TextInput(),
#         }


