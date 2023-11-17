from django.shortcuts import redirect, render

from kitchenrun.forms import EventPropertyForm, CourseForm
from kitchenrun.models import EventProperty, Team, Course
from main.models import Event
from networkx.algorithms import bipartite

import random
import networkx as nx

# Create your views here.

def add_kitchenrun_property(request):
    if request.method == 'POST':
        form = EventPropertyForm(request.POST)
        if form.is_valid():
            eventProperty = form.save(commit=False)
            eventProperty.event = Event.objects.get(id = request.session.get('event_id'))
            eventProperty.save()

            request.session['number_of_courses'] = eventProperty.course_number
            request.session['event_property_id'] = eventProperty.id

            return redirect('add_kitchenrun_course')  # Redirect to the event dashboard or other page
    else:
        form = EventPropertyForm()
    return render(request, 'add_kitchenrun_property.html', {'form': form})

def add_kitchenrun_course(request):
    if request.method == 'POST':
        forms = list()
        for i in range(request.session.get('number_of_courses')):
            forms.append(CourseForm(request.POST, prefix=i))
        

        for i in range(len(forms)):
            if forms[i].is_valid():
                course = forms[i].save(commit=False)
                course.event_property = EventProperty.objects.get(id = request.session.get('event_property_id'))
                course.order = i
                course.save()

        return redirect('view_index')  # Redirect to the event dashboard or other page
           
        
    else:
        forms = list()
        for i in range(request.session.get('number_of_courses')):
            forms.append(CourseForm(prefix=i))
        return render(request, 'add_courses.html', {'forms': forms})

def pair_teams(request, event_id):
    event_property = EventProperty.objects.get(id=event_id)
    courses = Course.objects.filter(event_property=event_property)

    teams = Team.objects.filter(event=event_property)

    #shuffled_teams = list(teams)
    

    # number of teams need to be dividable by the number of courses
    assert len(teams) % event_property.course_number == 0
    pairs_per_course = (int) (len(teams) / event_property.course_number)

    # pair teams with courses -> use bipartite matching algorithm (allows to match by course preference later)
    B = nx.Graph()
    
    # add nodes of type teams
    nodes_teams = [team.id for team in teams]
    random.shuffle(nodes_teams)
    B.add_nodes_from(nodes_teams, bipartite=0)

    # add nodes of type courses
    nodes_courses = list()
    for course in courses:
        for i in range(pairs_per_course):
            nodes_courses.append(str(course.id) + "_" + str(i))
    random.shuffle(nodes_courses)
    B.add_nodes_from(nodes_courses, bipartite=1)

    # add connections between both types
    edges = list()
    for team_id in nodes_teams:
        for course_id_str in nodes_courses:
            parts = course_id_str.split("_")
            if len(parts) == 2 and parts[0].isdigit():
                course_id = int(parts[0])
                if not (team_id == 1 and course_id == 4):
                    edges.append((team_id, course_id_str))
                # add filter here!

    B.add_edges_from(edges)

    result = bipartite.maximum_matching(B)

    return render(request, 'pair_teams.html', {'result': result, 'courses': nodes_courses, 'teams':nodes_teams})



    # pair cooking teams of each course with other teams (remove teams that have already seen each other)


