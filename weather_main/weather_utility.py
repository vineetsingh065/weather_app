import requests
from django.conf import settings
from datetime import date
import calendar


def get_current_weather(city):

    weather_request_resp = requests.get(f'http://api.openweathermap.org/data/2.5/weather?'
                                        f'q={city}&appid={settings.OPEN_WEATHER_API_KEY}').json()
    if 'message' in weather_request_resp:
        return str(weather_request_resp['cod'])+" | "+weather_request_resp['message']
    my_date = date.today()
    day = calendar.day_name[my_date.weekday()]

    aqi_request = requests.get(f'http://api.airpollutionapi.com/1.0/aqi?'
                               f'lat={weather_request_resp["coord"]["lat"]}&'
                               f'lon={weather_request_resp["coord"]["lon"]}'
                               f'&APPID={settings.AQI_KEY}').json()
    data = {
        'weather': weather_request_resp['weather'][0]['main'],
        'temp': float("{:.2f}".format(weather_request_resp['main']['temp'] - 273.15)),
        'feels': float("{:.2f}".format(weather_request_resp['main']['feels_like'] - 273.15)),
        'wind': float("{:.2f}".format(weather_request_resp['wind']['speed'] * 3.6)),
        'day': day,
        'city': city,
        'dominating': aqi_request['data']['dominating'],
        'aqi_status': aqi_request['data']['text'],
        'aqi_alert': aqi_request['data']['alert'],
        'barometric': aqi_request['data']['aqiParams'][5]['value'],

    }

    for params in aqi_request['data']['aqiParams']:
        if params['name'] == aqi_request['data']['dominating']:
            data['aqi'] = params['name']+" "+str(params['aqi'])

    return data
