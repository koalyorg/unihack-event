from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404

from kitchenrun.forms import EventPropertyForm, TeamForm
from kitchenrun.models import EventProperty, Team, Pair
from main.models import Event
from networkx.algorithms import bipartite

import random
import networkx as nx

# Create your views here.

def add_kitchenrun_property(request):
    event = Event.objects.get(id = request.session.get('event_id'))
    event_property = EventProperty.objects.filter(event=event).first()
    if request.method == 'POST':
        form = EventPropertyForm(request.POST, instance=event_property)
        if form.is_valid():
            eventProperty = form.save(commit=False)
            eventProperty.event = event
            eventProperty.save()
            messages.success(request, "Event successfully updated.")
            # request.session['number_of_courses'] = eventProperty.course_number
            # request.session['event_property_id'] = eventProperty.id
            return redirect('event_detail', event_id=event.id)  # Redirect to the event dashboard or other page
    else:
        form = EventPropertyForm(instance=event_property)
    return render(request, 'add_kitchenrun_property.html', {'form': form})

def kitchenrun_signup(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = TeamForm(request.POST, instance=None)
        if form.is_valid():
            team = form.save(commit=False)
            team.event = event
            team.user = request.user
            team.save()
            event.participants.add(request.user)
            messages.success(request, "Team successfully created.")
            return redirect('event_detail', event_id=event.id)  # Redirect to the event dashboard or other page
    else:
        form = TeamForm(instance=None)
    return render(request, 'add_team.html', {'form': form})

@login_required
def kitchenrun_team_details(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    team =  get_object_or_404(Team, event=event, user=request.user)
    pairing = Pair.objects.all().filter(team=team)
    return render(request, 'team_details.html', {"event": event, "team": team, "pair": pairing})


# def add_kitchenrun_course(request):
#     event_property = EventProperty.objects.get(id=request.session.get('event_property_id'))
#     print(event_property)
#     courses_exist = Course.objects.filter(Q(event_property=event_property)).exists()
#     if courses_exist:
#         # todo make editable courses
#         return redirect('view_index')
#
#     if request.method == 'POST':
#         forms = list()
#         for i in range(request.session.get('number_of_courses')):
#             forms.append(CourseForm(request.POST, prefix=i))
#
#
#         for i in range(len(forms)):
#             if forms[i].is_valid():
#                 course = forms[i].save(commit=False)
#                 course.event_property = event_property
#                 course.order = i
#                 course.save()
#
#         return redirect('view_index')  # Redirect to the event dashboard or other page
#
#
#     else:
#         forms = list()
#         for i in range(request.session.get('number_of_courses')):
#             forms.append(CourseForm(prefix=i))
#         return render(request, 'add_courses.html', {'forms': forms})

def pair_teams(request, event_id):
    event = Event.objects.get(id=event_id)
    event_property = EventProperty.objects.filter(event=event).first()
    courses = ("Starter", "Main", "Desert")
    #courses = Course.objects.filter(event_property=event_property)

    teams = Team.objects.filter(event=event)

    #shuffled_teams = list(teams)


    # number of teams need to be dividable by the number of courses
    assert len(teams) % 3 == 0
    pairs_per_course = (int) (len(teams) / 3)

    # pair teams with courses -> use bipartite matching algorithm (allows to match by course preference later)
    B = nx.Graph()

    # add nodes of type teams
    nodes_teams = [team.id for team in teams]
    random.shuffle(nodes_teams)
    B.add_nodes_from(nodes_teams, bipartite=0)

    # add nodes of type courses
    nodes_courses = list()
    for course in Pair.COURSE_TYPES:
        course_id = course[0]
        for i in range(pairs_per_course):
            nodes_courses.append(str(course_id) + "_" + str(i))
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

    results = bipartite.maximum_matching(B)

    # create pair obj out of results
    cooking_teams = (list(), list(), list())
    for team_id, course_id_str in results.items():
        if isinstance(team_id, int) and isinstance(course_id_str, str):
            parts = course_id_str.split("_")
            if len(parts) == 2 and parts[0].isdigit():
                course_id = int(parts[0])
                cooking_teams[course_id].append(Team.objects.get(id=team_id))
                #pair = Pair(
                #    event = event_property,
                #    course = course_id,
                #    team = Team.objects.get(id=team_id),
                #    is_cook = True)
                #pair.save()


    # pair guest teams to cooking teams for each course by rotating the teams of the other courses
    for course in Pair.COURSE_TYPES:
        #cooking_pair = Pair.objects.filter(team=team, is_cook=True).first()
        #course = cooking_pair.course

        course_id = course[0]

        course_appetizer = 0
        course_main = 1
        course_dessert = 2

        if course_id == course_appetizer:
            for i in range(pairs_per_course):
                team = cooking_teams[course_appetizer][i]
                pair = Pair(
                    event = event,
                    course = course_id,
                    cook = team,
                    guest_1 = cooking_teams[course_main][i],
                    guest_2 = cooking_teams[course_dessert][i])
                pair.save()
        
        if course_id == course_main:  
            for i in range(pairs_per_course):
                team = cooking_teams[course_main][i]

                index1 = -1
                if (i+1 < pairs_per_course):
                    index1 = i+1
                else:
                    index1 = i-pairs_per_course+1

                index2 = -1
                if (i+2 < pairs_per_course):
                    index2 = i+2
                else:
                    index2 = i-pairs_per_course+2

                pair = Pair(
                    event = event,
                    course = course_id,
                    cook = team,
                    guest_1 = cooking_teams[course_appetizer][index1],
                    guest_2 = cooking_teams[course_dessert][index2])
                pair.save()

        if course_id == course_dessert:
            for i in range(pairs_per_course):
                team = cooking_teams[course_dessert][i]

                index1 = -1
                if (i+1 < pairs_per_course):
                    index1 = i+1
                else:
                    index1 = i-pairs_per_course+1

                index2 = -1
                if (i+2 < pairs_per_course):
                    index2 = i+2
                else:
                    index2 = i-pairs_per_course+2

                pair = Pair(
                    event = event,
                    course = course_id,
                    cook = team,
                    guest_1 = cooking_teams[course_appetizer][index1],
                    guest_2 = cooking_teams[course_main][index2])
                pair.save()

    #pairs = Pair.objects.filter(event=event_property)

    #w, h = len(teams), len(teams)
    #Matrix = [[0 for x in range(w)] for y in range(h)] 
    #works = True
    #for pair1 in pairs:
    #    for pair2 in pairs:
    #        if  pair1 != pair2 and pair1.pair_id == pair2.pair_id:
    #            Matrix[pair1.team.id-1][pair2.team.id-1] = Matrix[pair1.team.id-1][pair2.team.id-1] + 1

    #print(Matrix)
    messages.success(request, "Teams were successfully paired.")

    return redirect('event_detail', event_id=event_id)