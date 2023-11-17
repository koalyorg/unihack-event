from django.urls import path

from . import views
from .views import add_event
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='view_index'),
    path('add/', add_event, name='add_event'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('event/<int:event_id>/register/', views.register_for_event, name='register_for_event'),
    path('event/<int:event_id>/deregister/', views.deregister_for_event, name='deregister_for_event'),
    path('event/<int:event_id>/', views.event, name='event_detail'),

]