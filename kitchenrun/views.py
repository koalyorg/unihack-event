from django.shortcuts import redirect, render

from kitchenrun.forms import EventPropertyForm, CourseForm
from kitchenrun.models import EventProperty
from main.models import Event

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