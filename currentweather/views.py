from django.shortcuts import render

import json
import requests

import calendar
from datetime import datetime
# Create your views here.


#To find Date
def findDate(dt_obj):
    date = dt_obj.strftime("%d %B, %Y")
    return date

#To find Time
def findTime(dt_obj):
    time = dt_obj.strftime("%H:%M:%S")
    return time

#To find Day
def findDay(dt_obj):
	day = dt_obj.strftime("%A")
	return day
	
	'''
    date = dt_obj.strftime("%Y-%m-%d")
    year, month, day = (int(i) for i in date.split('-'))     
    day_num = calendar.weekday(year, month, day) 
    days =["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"] 

    return (days[day_num])
	'''


def home(request):

	city = "lucknow"
	if request.method == "POST":
		city = request.POST['city']

	api_key = 'bd92abff74544a4daa2b86a90930810f'
	URL = 'http://api.openweathermap.org/data/2.5/weather'#?q=' + city + '&appid=' + api_key
	PARAMS = {'q': city, 'appid': api_key}
	api_request = requests.get(url = URL, params = PARAMS)

	try:
		api = json.loads(api_request.content)
	except Exception as e:
		api = "ERROR"

	if api == "ERROR" or api['cod'] == "404":
		return render(request, 'home.html', {'res': "ERROR"})
	else:
		dt_obj = datetime.fromtimestamp(api['dt'])

		day = findDay(dt_obj)
		time = findTime(dt_obj)
		date = findDate(dt_obj)

		#temp's Unit is Kelvin here
		temp = api['main']['temp']
		temp = int(temp - 273.15)

		city = api['name']
		country = api['sys']['country']

		weather = api['weather'][0]['description']
		humidity = api['main']['humidity']
		pressure = api['main']['pressure']
		cloudy = api['clouds']['all']
		wind = api['wind']['speed']


		#respone -> res
		res = {}
		res['time'] = time
		res['day'] = day
		res['date'] = date
		res['temp'] = temp
		res['city'] = city
		res['country'] = country

		res['weather'] = weather
		res['humidity'] = humidity
		res['pressure'] = pressure
		res['cloudy'] = cloudy
		res['wind'] = wind

		return render(request, 'home.html', {'res': res})

def about(request):
	return render(request, 'about.html', {})