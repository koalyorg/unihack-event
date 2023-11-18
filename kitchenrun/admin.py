from django.contrib import admin

from .models import EventProperty, Team, TeamMember, Course, Pair 

# Register your models here.

admin.site.register(EventProperty)
admin.site.register(Team)
admin.site.register(TeamMember)
admin.site.register(Course)
admin.site.register(Pair)
