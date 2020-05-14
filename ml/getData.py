import pprint
import json
import populartimes
import APIKey
import datetime

import requests

'''
Map the weather response code to the probability of going out
Note: this is currently done purely on my judgement
1 = I'm going out to have a BBQ and beer right now
0.1 = not going outside staying in bed
(0.1 rather than 0 for smoothing reasons)
'''
weather_dictionary = {
    200: 0.3,  # Thunderstorm with light rain
    201: 0.3,  # Thunderstorm with rain
    202: 0.1,  # Thunderstorm with heavy rain
    230: 0.3,  # Thunderstorm  with light drizzle
    231: 0.2,  # Thunderstorm with drizzle
    232: 0.1,  # Thunderstorm with heavy drizzle
    233: 0.1,  # Thunderstorm with hail
    300: 0.7,  # light drizzle
    301: 0.6,  # drizzle
    500: 0.6,  # light rain
    501: 0.5,  # moderate rain
    502: 0.3,  # heavy rain
    511: 0.1,  # freezing rain
    520: 0.6,  # light shower rain
    521: 0.5,  # shower rain
    522: 0.2,  # heay shower rain
    600: 0.2,  # light snow
    601: 0.2,  # snow
    602: 0.1,  # heavy snow
    610: 0.1,  # snow rain
    611: 0.2,  # sleet
    612: 0.1,  # heavy sleet
    621: 0.1,  # snow shower
    622: 0.1,  # heavy snow shower
    623: 0.3,  # flurries
    700: 0.7,  # mist
    711: 0.7,  # smoke
    721: 0.7,  # haaze
    731: 0.7,  # sand/dust
    741: 0.7,  # fog
    751: 0.5,  # freezing fog
    800: 1.0,  # clear sky
    801: 0.95,  # few clouds
    802: 0.9,  # scattered clouds
    803: 0.8,  # broken clouds,
    804: 0.75,  # overcas clouds,
    900: 0.4  # unknown precip
}

name = ''
lat = 0.0
long = 0.0
type_place = []
opening_times = []


def googleData(placeID):
    global lat
    global long
    global type_place
    global name

    api_key = APIKey.getGoogleAPIKey()
    url = 'https://maps.googleapis.com/maps/api/place/details/json?place_id=' + placeID + '&fields=formatted_address,name,type,opening_hours,geometry&key=' + api_key
    get_data = requests.get(url).json()['result']

    if 'name' in get_data:
        name = get_data['name']
    else:
        name = get_data['formatted_address']

    if 'types' in get_data:
        type_place = get_data['types']

    if 'opening_hours' in get_data:
        # open hours will reduce forecast to 0 outside open hours
        openhours = convertOpenHours(get_data['opening_hours']['weekday_text'])
    else:
        # open hours will not affect the output forecast since we do not know them
        openhours = ['0', '23']

    latlong = get_data['geometry']['location']
    lat = latlong['lat']
    long = latlong['lng']

    return [lat, long, openhours]


def getPopularTimes(placeID):
    current_estimate = 1
    forecast = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    api_key = APIKey.getGoogleAPIKey()

    pop_times = populartimes.get_id(api_key, placeID)

    if 'populartimes' in pop_times:
        # return the prediction for today's forecast courtesy of Google Maps
        forecast = pop_times['populartimes'][datetime.date.today().weekday()].get('data')

    if 'current_popularity' in pop_times:
        current_estimate = pop_times['current_popularity']

    elif 'populartimes' in pop_times:
        current_estimate = forecast[datetime.datetime.now().hour]

    return [forecast, current_estimate]


def getWeather(lat, lon):
    api_key = APIKey.getWeatherKey()
    url = 'https://api.weatherbit.io/v2.0/forecast/hourly?lat=' + str(lat) + '&lon=' + str(
        lon) + '&key=' + api_key + '&hours=24'
    weather_data = requests.get(url).json()

    temps = []
    forecast = []
    chanceRain = []

    for hour in weather_data['data']:
        temps.append((hour['app_temp'] + 3) / (31))  # normalising, 34 highest, -3 lowest
        get_forecast = hour['weather']['code']
        forecast.append(weather_dictionary[get_forecast])
        chanceRain.append(1 - (hour['precip'] / 210))  # normalising, 210 highest recorded value this year

    # need to rotate arrays so midnight-midnight
    slice = datetime.datetime.now().hour
    temps = temps[slice:] + temps[:slice]
    forecast = forecast[slice:] + forecast[:slice]
    chanceRain = chanceRain[slice:] + chanceRain[:slice]

    return [temps, forecast, chanceRain]


def convertOpenHours(data):
    try:
        today = data[datetime.date.today().weekday()]
        today = today.split("day: ")[1].split(" – ")
        open = today[0].split(" ")
        closed = today[1].split(" ")
        open[0] = open[0].split(":")[0]
        closed[0] = closed[0].split(":")[0]
        if open[1] == 'PM':
            open[0] = int(open[0]) + 12
        if closed[1] == 'PM':
            closed[0] = int(closed[0]) + 12
        if closed == ['12', 'AM']:
            closed = ['0', 'AM']
        return [open[0], closed[0]]
    except:
        return [0, 23]


def getPlaceName():
    return name