from django.shortcuts import render
import requests
from django.conf import settings

from datetime import date
import calendar

# Create your views here.


def home(request):

    if request.method == "POST":
        city = request.POST['location']

        weather_request_resp = requests.get(f'http://api.openweathermap.org/data/2.5/weather?'
                                            f'q={city}&appid={settings.OPEN_WEATHER_API_KEY}').json()
        my_date = date.today()
        day = calendar.day_name[my_date.weekday()]

        data = {
            'weather': weather_request_resp['weather'][0]['main'],
            'temp': float("{:.2f}".format(weather_request_resp['main']['temp'] - 273.15)),
            'feels': float("{:.2f}".format(weather_request_resp['main']['feels_like'] - 273.15)),
            'wind': float("{:.2f}".format(weather_request_resp['wind']['speed'] * 3.6)),
            'day': day,
            'city': city,

        }
    else:
        data = {}

    return render(request, template_name='index.html', context=data)


