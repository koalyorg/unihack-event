from django import forms
from .models import Event
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['owner', 'participants', 'lat', 'lon']  # Excluding parts of event that aren't part of the form
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'registration_end': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'duration': forms.TimeInput(format='%H'),
            'description': forms.Textarea(attrs={'rows': 4}),
            # Define other widgets as needed
        }
        labels = {
            'start_time': 'Event Start Time',
            'registration_end': 'Registration Deadline',
            'duration': "Duration in hours"
            # Other labels
        }
        help_texts = {
            'description': 'Describe the event in detail.',
            # Other help texts
        }


