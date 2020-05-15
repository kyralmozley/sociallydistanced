#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import math

import getData

currentPrediction = 0
day_forecast = [0]*24
google_ranking = 0
weather_ranking = 0
temps = []
forecast = []
chance_rain = []
trend_rate = 0
tweet_rate = 0

def makePrediction(placeID):
    global currentPrediction
    global day_forecast

    global google_ranking
    global weather_ranking
    global temps
    global forecast
    global chance_rain
    global trend_rate
    global tweet_rate

    weather_weighting = 1.2

    [lat, long, openhours] = getData.googleData(placeID)

    google_ranking = getData.getPopularTimes(placeID)  # returns [forecast, current]
    weather_ranking = getData.getWeather(lat, long)

    # combine weather ranking
    [temps, forecast, chance_rain] = weather_ranking
    combine = [a * b for a, b in zip(temps, forecast)]
    combine = [a * b for a, b in zip(combine, chance_rain)]

    # if place is a park, weather is weighted more strongly
    # else it shouldnt add much of an effect
    # weather is working with decimals !
    place = getData.getTypePlace()
    name = getData.getPlaceName()
    name= name.split("-")[0]
    trend_weight = getData.getTrends(name)
    tweet_weight = getData.getTweets(name)
    tweet_weight = math.log(tweet_weight +1, 100)
    if tweet_weight < 0.1:
        tweet_weight = 0.1

    if 'supermarket' in place or 'store' in place or 'grocery_or_supermarket' in place or 'liquor_store' in place:
        weather_weighting = 1.3
        tweet_weight = 1
    if 'park' in place:
        weather_weighting = 0.8

    if trend_weight == 0:
        # assume something went wrong in finding the trend, do nothing
        trend_weight = 1
    else:
        trend_weight = math.log(trend_weight+1, 10)
    if google_ranking[0] != day_forecast: # not a load of zeros
        combine = [a * b for a, b in zip(combine, google_ranking[0])]
        combine = [i * weather_weighting * trend_weight * tweet_weight for i in combine]
    else:
        combine = [i * weather_weighting * trend_weight * tweet_weight * 50 for i in combine]




    for x in range(0, int(openhours[0])):
        combine[x] = 0
    if int(openhours[1]) != 0:
        for x in range(int(openhours[1]), 24):
            combine[x] = 0

    shift = datetime.date.today().weekday()

    currentPrediction = 2 * google_ranking[1] * temps[shift] * forecast[shift] * chance_rain[shift] * weather_weighting * trend_weight * tweet_weight
    day_forecast = combine


def getCurrentPrediction():
    if currentPrediction > 40:
        return 4
    elif currentPrediction > 30:
        return 3
    elif currentPrediction > 15:
        return 2
    elif currentPrediction > 5:
        return 1
    else:
        return 0


def getDayForecast():
    for i in range(len(day_forecast)):
        if day_forecast[i] > 99:
            day_forecast[i] = 99
        day_forecast[i] = int(day_forecast[i])
    return day_forecast

def getPlaceName():
    return getData.getPlaceName()

def getIsOpen():
    return getData.getIsOpen()

def getGoogleRanking():
    return google_ranking
def getWeatherRanking():
    return weather_ranking
def getTemps():
    return temps
def getForecast():
    return forecast
def getChanceRain():
    return chance_rain
def getTrendRate():
    return trend_rate
def getTweetRate():
    return tweet_rate
