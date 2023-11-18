from django import forms
from .models import EventProperty, Team
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


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        exclude = ['event', 'user']  # Excluding owner and participants
        widgets = {

        }
        labels = {
           'name': "Team Name",
            'street': "Street",
            'number': "Housenumber",
            'team_member_1': "Name of the first team member",
            'team_member_2': "Name of the second team member"

        }
        help_texts = {
            'address_addition': "Address Additions as apartment number or other useful information for finding the address.",
            'is_vegan': "In case one team member is vegetarian activate this checkbox.",
            'is_vegetarian': "In case one team member is vegan activate this checkbox.",
            'is_halal': "In case one team member is halal activate this checkbox.",
            'is_kosher': "In case one team member is kosher activate this checkbox.",
            'comments': "In case you have anything to tell, please provide it here.",


        }

#
# class CourseForm(forms.ModelForm):
#     class Meta:
#         model = Course
#         exclude = ['event_property', 'order']
#         widgets = {
#             'name': forms.TextInput(),
#         }


