from django.shortcuts import render
from .models import Event
# Create your views here.

def index(request):
    if request.user.is_authenticated:
        events = Event.objects.all().order_by('start_time')  # Fetch events ordered by start time
        return render(request, 'dashboard.html', {'events': events})
    else:
        return render(request, 'index.html')
