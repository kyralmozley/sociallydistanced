#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pprint
import json
import populartimes
import APIKey
import datetime
from pytrends.request import TrendReq
import requests
import pandas as pd
import tweepy


name = ''
lat = 0.0
long = 0.0
type_place = []
opening_times = []
open_now = True


def googleData(placeID):
    # declare global variables
    global lat
    global long
    global type_place
    global name
    global open_now

    # request data from Google
    api_key = APIKey.getGoogleAPIKey()
    url = 'https://maps.googleapis.com/maps/api/place/details/json?place_id=' + placeID + '&fields=formatted_address,name,type,opening_hours,geometry&key=' + api_key
    get_data = requests.get(url).json()['result']

    # Get googles name for the place
    if 'name' in get_data:
        name = get_data['name']
    else:
        # If no name exists, use their formatted address
        name = get_data['formatted_address']

    if 'types' in get_data:
        type_place = get_data['types']

    if 'opening_hours' in get_data:
        # open hours will reduce forecast to 0 outside open hours
        openhours = convertOpenHours(get_data['opening_hours']['weekday_text'])
        open_now = get_data['opening_hours']['open_now']
    else:
        # Google doesn't provide data, so open hours will not affect the output forecast
        openhours = ['0', '23']

    # get latlong
    latlong = get_data['geometry']['location']
    lat = latlong['lat']
    long = latlong['lng']

    return openhours


def getPopularTimes(placeID):
    # default current estimates
    current_estimate = -1
    forecast = [0.0] * 24

    api_key = APIKey.getGoogleAPIKey()

    # request popular times from google
    pop_times = populartimes.get_id(api_key, placeID)

    if 'populartimes' in pop_times:
        # return the prediction for today's forecast courtesy of Google Maps
        forecast = pop_times['populartimes'][datetime.date.today().weekday()].get('data')

    if 'current_popularity' in pop_times:
        current_estimate = pop_times['current_popularity']

    return [forecast, current_estimate]


def getWeather():
    # request weather data from weatherbit
    api_key = APIKey.getWeatherKey()
    url = 'https://api.weatherbit.io/v2.0/forecast/hourly?lat=' + str(lat) + '&lon=' + str(
        long) + '&key=' + api_key + '&hours=24'
    weather_data = requests.get(url).json()

    # define arrays to return
    feels_like = []
    temps = []
    cloud = []
    forecast = []
    chanceRain = []

    # add the required weather data per hour
    for hour in weather_data['data']:
        temps.append(hour['temp'])
        feels_like.append(hour['app_temp'])
        forecast.append(hour['weather']['code'])
        chanceRain.append(hour['precip'])
        cloud.append(hour['clouds'])

    # need to rotate arrays so midnight-midnight
    slice = datetime.datetime.now().hour
    temps = temps[slice:] + temps[:slice]
    forecast = forecast[slice:] + forecast[:slice]
    chanceRain = chanceRain[slice:] + chanceRain[:slice]

    return [feels_like, temps, cloud, forecast, chanceRain]


def getTrends(name):
    # get google search trends
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        kw_list = [name]
        pytrends.build_payload(kw_list, cat=0, timeframe='today 3-m', geo='GB-ENG', gprop='')
        week_trends = pytrends.interest_over_time().iloc[-1, 0]  # yesterdays score (sadly doesnt give todays)

        pytrends.build_payload(kw_list, cat=0, timeframe='now 7-d', geo='GB-ENG', gprop='')
        day_trends = pytrends.interest_over_time().tail(24).mean()[0]
        return [week_trends, day_trends]
    except:
        return [0,0]


def getTweets(place):
    try:
        auth = tweepy.OAuthHandler(APIKey.getTwitterAPIKey(), APIKey.getTwitterSecretKey())
        auth.set_access_token(APIKey.getTwitterAccessToken(), APIKey.getTwitterAccessTokenSecret())
        api = tweepy.API(auth, wait_on_rate_limit=False, wait_on_rate_limit_notify=True)

        placeID = api.reverse_geocode(lat, long, 1000)
        tweets = []

        startDate = datetime.datetime.now() - datetime.timedelta(hours = 24)
        endDate = datetime.datetime.now()

        # get first tweet at location/name to get ID
        tweet = api.search(q=place + '-filter:retweets', geo=placeID, count=1)

        tweet_id = str(tweet[-1]).split(',')
        id = int(tweet_id[2].split(":")[1])

        loop = 1
        while loop < 5:
            tweet = api.search(q=place + '-filter:retweets', geo=placeID, count=100, max_id=id-1)
            if not tweet:
                break

            tweet_id = str(tweet[-1]).split(',')

            for t in tweet:
                if endDate > t.created_at > startDate:
                    tweets.append(t)
                else:
                    break

            id = int(tweet_id[2].split(":")[1])

            loop += 1

        return len(tweets)
    except:
        return 1


def convertOpenHours(data):
    try:
        # try to split the horrifying "Monday: 09:00AM - 11:00PM" into [9, 23]
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


def getTypePlace():
    return type_place


def getIsOpen():
    return open_now
