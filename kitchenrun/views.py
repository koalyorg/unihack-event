from django.shortcuts import redirect, render

from kitchenrun.forms import EventPropertyForm, CourseForm
from kitchenrun.models import EventProperty, Team, Course, Pair
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

    results = bipartite.maximum_matching(B)

    # create pair obj out of results
    teams_sorted = (list(), list(), list())
    for team_id, course_id_str in results.items():
        if isinstance(team_id, int) and isinstance(course_id_str, str):
            parts = course_id_str.split("_")
            if len(parts) == 2 and parts[0].isdigit():
                course_id = int(parts[0])
                teams_sorted[course_id-4].append(Team.objects.get(id=team_id))
                pair = Pair(
                    event = event_property,
                    course = Course.objects.get(id=course_id),
                    team = Team.objects.get(id=team_id),
                    is_cook = True)
                pair.save()


    for course in courses:
        #cooking_pair = Pair.objects.filter(team=team, is_cook=True).first()
        #course = cooking_pair.course

        course_appetizer = 0
        course_main = 1
        course_dessert = 2

        if course.id == 4:
            for i in range(pairs_per_course):
                team = teams_sorted[course_appetizer][i]
                pair_cook = Pair.objects.filter(event=event_property, course=course, team=team, is_cook=True).first()
                pair = Pair(
                    event = event_property,
                    course = course,
                    team = teams_sorted[course_main][i], # todo: adjust
                    is_cook = False,
                    pair_id = pair_cook.pair_id)
                pair.save()

                pair = Pair(
                    event = event_property,
                    course = course,
                    team = teams_sorted[course_dessert][i], # todo: adjust
                    is_cook = False,
                    pair_id = pair_cook.pair_id)
                pair.save()
        
        if course.id == 5:  
            for i in range(pairs_per_course):
                team = teams_sorted[course_main][i]
                pair_cook = Pair.objects.filter(event=event_property, course=course, team=team, is_cook=True).first()

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
                    event = event_property,
                    course = course,
                    team = teams_sorted[course_appetizer][index1], # todo: adjust
                    is_cook = False,
                    pair_id = pair_cook.pair_id)
                pair.save()

                pair = Pair(
                    event = event_property,
                    course = course,
                    team = teams_sorted[course_dessert][index2], # todo: adjust
                    is_cook = False,
                    pair_id = pair_cook.pair_id)
                pair.save()

        if course.id == 6:
            for i in range(pairs_per_course):
                team = teams_sorted[course_dessert][i]
                pair_cook = Pair.objects.filter(event=event_property, course=course, team=team, is_cook=True).first()

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
                    event = event_property,
                    course = course,
                    team = teams_sorted[course_appetizer][index1], # todo: adjust
                    is_cook = False,
                    pair_id = pair_cook.pair_id)
                pair.save()

                pair = Pair(
                    event = event_property,
                    course = course,
                    team = teams_sorted[course_main][index2], # todo: adjust
                    is_cook = False,
                    pair_id = pair_cook.pair_id)
                pair.save()

    pairs = Pair.objects.filter(event=event_property)

    w, h = len(teams), len(teams)
    Matrix = [[0 for x in range(w)] for y in range(h)] 
    works = True
    for pair1 in pairs:
        for pair2 in pairs:
            if  pair1 != pair2 and pair1.pair_id == pair2.pair_id:
                Matrix[pair1.team.id-1][pair2.team.id-1] = Matrix[pair1.team.id-1][pair2.team.id-1] + 1

    print(Matrix)
    return render(request, 'pair_teams.html', {'result': results, 'courses': nodes_courses, 'teams':nodes_teams})