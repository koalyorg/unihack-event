from django.urls import path

from . import views

urlpatterns = [
    path('add/', views.add_kitchenrun_property, name='add_kitchenrun_property'),
    path('add/course/', views.add_kitchenrun_course, name='add_kitchenrun_course'),
]


