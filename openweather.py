# coding=utf-8

"""
openweather.py - a weather tool to get weather data and store locations based on user names
Copyright 2016 - samuelvimes
Licensed under GNU GPL 3.0
https://github.com/samuelvimes
"""

from sopel.module import commands
import pyowm

owm = pyowm.OWM('YOUR_OPENWEATHER_API_KEY') #Get an API key at openweather.com

@commands('we','weather')
def weather(bot, trigger):
  location = trigger.group(2)
  cityid = ''
  if not location:
    cityid = bot.db.get_nick_value(trigger.nick, 'cityid')
    if not cityid:
      return bot.reply('I don\'t know where you live. ' +
                       'Give me a location, like ".weather London,UK" or ".weather 90403,DE" or tell me where you live by saying ".setlocation London,UK" for example.')
    current = owm.weather_at_id(cityid)
  else:
    current = owm.weather_at_place(location)

#Get the weather data
  w = current.get_weather()

  status = w.get_detailed_status()
  wind = w.get_wind()
  humidity = w.get_humidity()
  pressure = w.get_pressure()
  pressure = pressure['press']
  temp_c = w.get_temperature('celsius')
  temp_c = temp_c['temp']
  temp_f = w.get_temperature('fahrenheit')
  temp_f = temp_f['temp']
  sunrise = w.get_sunrise_time()
  sunset = w.get_sunset_time()
  clouds = w.get_clouds()
  rain = w.get_rain()
  snow = w.get_snow()
  
  wind_speed = wind['speed']
  speed = int(round(wind_speed, 0))
  
  if speed == 0:
    description = 'Calm'
  elif speed < 1:
    description = 'Light air'
  elif speed < 2:
    description = 'Light breeze'
  elif speed < 4:
    description = 'Gentle breeze'
  elif speed < 6:
    description = 'Moderate breeze'
  elif speed < 9:
    description = 'Fresh breeze'
  elif speed < 11:
    description = 'Strong breeze'
  elif speed < 14:
    description = 'Near gale'
  elif speed < 18:
    description = 'Gale'
  elif speed < 22:
    description = 'Strong gale'
  elif speed < 26:
    description = 'Storm'
  elif speed < 30:
    description = 'Violent storm'
  else:
    description = 'Hurricane'

  degrees = wind['deg']
  
  if (degrees <= 22.5) or (degrees > 337.5):
    degrees = u'\u2193'
  elif (degrees > 22.5) and (degrees <= 67.5):
    degrees = u'\u2199'
  elif (degrees > 67.5) and (degrees <= 112.5):
    degrees = u'\u2190'
  elif (degrees > 112.5) and (degrees <= 157.5):
    degrees = u'\u2196'
  elif (degrees > 157.5) and (degrees <= 202.5):
    degrees = u'\u2191'
  elif (degrees > 202.5) and (degrees <= 247.5):
    degrees = u'\u2197'
  elif (degrees > 247.5) and (degrees <= 292.5):
    degrees = u'\u2192'
  elif (degrees > 292.5) and (degrees <= 337.5):
    degrees = u'\u2198'

#Get the location data
  l = current.get_location()
  
  city = l.get_name()
  country = l.get_country()
  
  bot.reply(u'{0},{1}: {2} ({3}), {4}m/s ({5}), {6}°C ({7}°F), {8}%, {9}hpa'.format(city, country, status, description, wind_speed, degrees, temp_c, temp_f, humidity, pressure))

@commands('setlocation')
def update_cityid(bot, trigger):
  if not trigger.group(2):
    bot.say('Give me a location like London,UK or Washington,DC')
    return
  
  location_lookup = trigger.group(2)
  cityid_lookup = owm.weather_at_place(location_lookup)
  
  if cityid_lookup is None:
    bot.reply('I do not know where that is')
    return
	
  c = cityid_lookup.get_location()
  city_id = c.get_ID()
  city_name = c.get_name()
  city_country = c.get_country()
  bot.db.set_nick_value(trigger.nick, 'cityid', city_id)
  bot.reply('Your location has been set to {0},{1}'.format(city_name, city_country))
