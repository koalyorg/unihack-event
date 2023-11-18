from django.urls import path

from . import views

urlpatterns = [
    path('add/', views.add_kitchenrun_property, name='add_kitchenrun_property'),
#    path('add/course/', views.add_kitchenrun_course, name='add_kitchenrun_course'),
    path('<int:event_id>/pair', views.pair_teams, name='kitchenrun_pair_teams'),
    path('pair/', views.pair_teams, name="pair_teams")
]


