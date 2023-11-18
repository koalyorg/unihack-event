from django.urls import path

from . import views

urlpatterns = [
    path('add/', views.add_kitchenrun_property, name='add_kitchenrun_property'),
#    path('add/course/', views.add_kitchenrun_course, name='add_kitchenrun_course'),
    path('<int:event_id>/pair', views.pair_teams, name='kitchenrun_pair_teams'),
    path('<int:event_id>/team', views.kitchenrun_signup, name='kitchenrun_signup'),
    path('<int:event_id>/team-details', views.kitchenrun_team_details, name='kitchenrun_team_details'),
    path('pair/', views.pair_teams, name="pair_teams")
]


