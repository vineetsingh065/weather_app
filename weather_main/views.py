from django.shortcuts import render, redirect
from django.contrib import messages
from .weather_utility import get_current_weather

# Create your views here.


def home(request):

    if request.method == "POST":
        city = request.POST['location']
        data = get_current_weather(city)
        if type(data) == str:
            messages.error(request, data)
            return redirect('home')
    else:
        data = {}

    return render(request, template_name='index.html', context=data)


