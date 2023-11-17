from django.contrib import admin
from .models import Event

# Register your models here.

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'start_time', 'end_time', 'timezone', 'organizer', 'participant_count')
    list_filter = ('event_type', 'timezone', 'organizer')
    search_fields = ('title', 'description', 'organizer')
    ordering = ('start_time',)
    date_hierarchy = 'start_time'
    # Add more customizations as needed


admin.site.register(Event, EventAdmin)
