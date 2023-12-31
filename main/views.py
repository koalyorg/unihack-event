from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from kitchenrun.models import Team
from .models import Event
from .forms import EventForm, MessageForm
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
        events = Event.objects.filter(Q(public=True) & Q(approved=True))
        if query:
            events = events.filter(Q(city__icontains=query) | Q(is_virtual=True)).order_by('start_time')
        else:
            events = Event.objects.all().order_by('start_time')
        past = request.GET.get('past', '')
        if len(past) > 0:
            pass
        else:
           events = [x for x in events if x.status_code <= 4]
        own = request.GET.get('own', '')
        if len(own) > 0:
            events = Event.objects.all().filter(Q(owner=request.user)).order_by('start_time')
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
            messages.success(request, "Welcome to UnityEvents!")
            return redirect('view_index')  # Redirect to a home page or another appropriate page
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def add_event(request, event_id=None):
    event = None
    if event_id:
        event = get_object_or_404(Event, id=event_id)
    form = EventForm(instance=event)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            event.owner = request.user  # Set the event owner to the current user
            if not event.is_virtual:
                try:
                    event.generate_geo()
                except:
                    form.add_error('location', 'Location was invalid')
                    messages.error(request, "Location was invalid")
                    return render(request, 'add_event.html', {'form': form})
            event.save()
            # two step form if Kitchen Run
            if event.event_type == 'KITCHENRUN':
                request.session['event_id'] = event.id
                return redirect('add_kitchenrun_property')
            if event:
                messages.success(request, "Event successfully updated.")
            else:
                messages.success(request, "Event successfully created.")
            return redirect('view_index')  # Redirect to the event dashboard or other page
    return render(request, 'add_event.html', {'form': form})

@login_required
def delete_event(request, event_id):
    user = request.user
    event = get_object_or_404(Event, pk=event_id)
    if user.is_superuser or event.owner == user:
        event.delete()
    messages.success(request, "Event successfully deleted.")
    return redirect('view_index')


def map_test(request):
    coordinates = [45.7499, 21.2071]
    return render(request, 'map.html', {'dest': coordinates})

@login_required
def register_for_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if event.can_add_participant():
        if event.event_type == "KITCHENRUN":
            return redirect('kitchenrun_signup', event_id=event_id)
        event.participants.add(request.user)
        messages.success(request, "Successfully registered")
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
        if event.event_type == "KITCHENRUN":
            team = get_object_or_404(Team, user=request.user, event=event)
            team.delete()
        messages.success(request, "Event successfully deregistered.")
    else:
        # Handle the case where the event is full or the user can't be added
        pass
    return redirect('event_detail', event_id=event.id)

def event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        user = request.user
        if user.is_superuser or event.owner == user:
            form = MessageForm(request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.event = event
                message.owner = user
                message.save()
                messages.success(request, "Message successfully sent.")
    form = MessageForm()

    # get coordinates
    coordinates = [float(event.lat), float(event.lon)]

    return render(request, 'event.html', {'event': event, 'form': form, 'coordinates': coordinates})


def about(request):
    return render(request, 'about.html')