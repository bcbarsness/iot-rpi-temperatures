#!/usr/bin/python3

from urllib import urlopen
import json

#apikey="XXXXXXXXXXX" # sign up here http://www.wunderground.com/weather/api/ for a key
url="http://api.openweathermap.org/data/2.5/weather?zip=23507,us&APPID=%s" % sys.argv[2]
meteo=urlopen(url).read()
meteo = meteo.decode('utf-8')
weather = json.loads(meteo)
print (weather['main']['temp'])
temp_f = (float(weather['main']['temp']) - 273.15) * 1.8 + 32
print (temp_f)
