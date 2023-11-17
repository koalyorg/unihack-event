from django.shortcuts import render

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        context = {}
        return render(request, 'dashboard.html', context)
    else:
        return render(request, 'index.html')
