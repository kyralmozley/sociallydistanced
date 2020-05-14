import pprint

import populartimes
import APIKey
import datetime

import requests

'''
Map the weather response code to the probability of going out
Note: this is currently done purely on my judgement 
1 = I'm going out to have a BBQ and beer right now
0.01 = not going outside staying in bed 
(0.01 rather than 0 for smoothing reasons)
'''
weather_dictionary = {
    200: 0.1,  # Thunderstorm with light rain
    201: 0.1,  # Thunderstorm with rain
    202: 0.01,  # Thunderstorm with heavy rain
    230: 0.1,  # Thunderstorm  with light drizzle
    231: 0.1,  # Thunderstorm with drizzle
    232: 0.01,  # Thunderstorm with heavy drizzle
    233: 0.01,  # Thunderstorm with hail
    300: 0.7,  # light drizzle
    301: 0.6,  # drizzle
    500: 0.5,  # light rain
    501: 0.4,  # moderate rain
    502: 0.1,  # heavy rain
    511: 0.05,  # freezing rain
    520: 0.6,  # light shower rain
    521: 0.4,  # shower rain
    522: 0.05,  # heay shower rain
    600: 0.1,  # light snow
    601: 0.1,  # snow
    602: 0.1,  # heavy snow
    610: 0.1,  # snow rain
    611: 0.1,  # sleet
    612: 0.05,  # heavy sleet
    621: 0.1,  # snow shower
    622: 0.01,  # heavy snow shower
    623: 0.3,  # flurries
    700: 0.7,  # mist
    711: 0.6,  # smoke
    721: 0.7,  # haaze
    731: 0.6,  # sand/dust
    741: 0.6,  # fog
    751: 0.5,  # freezing fog
    800: 1.0,  # clear sky
    801: 0.95,  # few clouds
    802: 0.9,  # scattered clouds
    803: 0.8,  # broken clouds,
    804: 0.7,  # overcas clouds,
    900: 0.2  # unknown precip
}

def googleLatLongtoPlaceID(lat, long):
    api_key = APIKey.getGoogleAPIKey()
    url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng=' + str(lat) + ',' + str(long) + '&key=' + api_key
    google_data = requests.get(url).json()
    return google_data['results'][0]['place_id']

def googlePlaceIDtoLatLong(placeID):
    api_key = APIKey.getGoogleAPIKey()
    url = 'https://maps.googleapis.com/maps/api/geocode/json?place_id=' + placeID + '&key=' + api_key
    google_data = requests.get(url).json()

    latlong = google_data['results'][0]['geometry']['location']
    return [latlong['lat'], latlong['lng']]


def getPopularTimes(placeID):
    current_estimate = 0
    forecast = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    api_key = APIKey.getGoogleAPIKey()

    pop_times = populartimes.get_id(api_key, placeID)
    #pprint.pprint(pop_times)

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
        temps.append((hour['app_temp'] + 3) / (31)) # normalising, 34 highest, -3 lowest
        get_forecast = hour['weather']['code']
        forecast.append(weather_dictionary[get_forecast])
        chanceRain.append(1 - (hour['precip'] / 210)) #normalising, 210 highest recorded value this year

    # need to rotate arrays so midnight-midnight
    slice = datetime.datetime.now().hour
    temps = temps[slice:] + temps[:slice]
    forecast = forecast[slice:] + forecast[:slice]
    chanceRain = chanceRain[slice:] + chanceRain[:slice]

    return [temps, forecast, chanceRain]
