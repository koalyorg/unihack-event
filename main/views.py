from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import Event
from .forms import EventForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from kitchenrun.forms import EventPropertyForm
from decimal import Decimal
import requests

def index(request):
    if request.user.is_authenticated:
        query = request.GET.get('q', '')
        print(query)
        if query:
            events = Event.objects.filter(Q(city__icontains=query) | Q(is_virtual=True)).order_by('start_time')
        else:
            events = Event.objects.all().order_by('start_time')
        past = request.GET.get('past', '')
        if len(past) > 0:
            pass
        else:
           events = [x for x in events if x.status_code <= 4]
        return render(request, 'dashboard.html', {'events': events})
    else:
        return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('view_index')  # Redirect to a home page or another appropriate page
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        form_step_2 = EventPropertyForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.owner = request.user  # Set the event owner to the current user

            # Get coordinates (lat, lon) from location
            if not event.is_virtual:
                api_url = "https://nominatim.openstreetmap.org/"
                # get lan, lon
                api_operator = "search"
                api_query = {"q": event.location, "format": "jsonv2", "accept-language": "en"}
                api_response = requests.get(api_url + api_operator, params=api_query)
                # todo check repsonse
                event.lat = Decimal(api_response.json()[0]['lat'])
                event.lon = Decimal(api_response.json()[0]['lon'])
                # get town
                api_operator = "reverse"
                api_query = {"lat": event.lat, "lon": event.lon, "format": "jsonv2", "accept-language": "en"}
                api_response = requests.get(api_url + api_operator, params=api_query)
                # todo check repsonse
                print(api_response.content)
                try:
                    event.city = api_response.json()["address"]['city']
                except:
                    event.city = api_response.json()["address"]['town']
                # Save form if inputs are valid
                event.save()
            else:
                event.save()

            # two step form if Kitchen Run
            if event.event_type == 'KITCHENRUN':
                request.session['event_id'] = event.id
                return redirect('add_kitchenrun_property')

            
            return redirect('view_index')  # Redirect to the event dashboard or other page
    else:
        form = EventForm()
    return render(request, 'add_event.html', {'form': form})

def map_test(request):
    coordinates = [50.6829, 10.9377]
    return render(request, 'map_test.html', {'dest': coordinates})

@login_required
def register_for_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if event.can_add_participant():
        event.participants.add(request.user)
        # Optionally, you can add a message or notification for the user
    else:
        # Handle the case where the event is full or the user can't be added
        pass
    return redirect('event_detail', event_id=event.id)

@login_required
def deregister_for_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.user in event.participants.all():
        event.participants.remove(request.user)
    else:
        # Handle the case where the event is full or the user can't be added
        pass
    return redirect('event_detail', event_id=event.id)



def event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'event.html', {'event': event})

def about(request):
    return render(request, 'about.html')