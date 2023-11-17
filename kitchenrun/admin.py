from django.contrib import admin

from .models import EventProperty, Team, TeamMember

# Register your models here.

admin.site.register(EventProperty)
admin.site.register(Team)
admin.site.register(TeamMember)
