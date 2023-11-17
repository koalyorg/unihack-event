from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Event
from .forms import EventForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm

def index(request):
    if request.user.is_authenticated:
        events = Event.objects.all().order_by('start_time')  # Fetch events ordered by start time
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
        if form.is_valid():
            event = form.save(commit=False)
            event.owner = request.user  # Set the event owner to the current user
            event.save()
            return redirect('view_index')  # Redirect to the event dashboard or other page
    else:
        form = EventForm()
    return render(request, 'add_event.html', {'form': form})


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
