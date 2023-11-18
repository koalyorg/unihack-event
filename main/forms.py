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
        exclude = ['owner', 'participants', 'lat', 'lon', 'city']  # Excluding parts of event that aren't part of the form
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'registration_end': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'duration': forms.TextInput(attrs={'placeholder': 'HH:MM:SS'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            # Define other widgets as needed
        }
        labels = {
            'start_time': 'Event Start Time',
            'registration_end': 'Registration Deadline',
            'duration': "Duration",
            'virtual_link': "Link for event (in case virtual)",
            'event_url': "External URL for Event",
            # Other labels
        }
        help_texts = {
            'description': 'Describe the event in detail.',
            'location': 'Provide a full address for in-person events, e.g. Piața Consiliul Europei 2D, Timișoara 300627, Romania or for online the used tool, e.g. zoom',
            'organizer': 'Name of the organizer / organisation',
            'virtual_link': "Provide e.g. a zoom link",
            'event_url': "Provide a URL to an external site for more information"
        }


