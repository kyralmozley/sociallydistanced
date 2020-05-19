#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import datetime
import math
import pickle
import pprint
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import getData

currentPrediction = 0
day_forecast = [0]*24
google_ranking = 0
weather_ranking = 0
place = []
temps = []
forecast = []
chance_rain = []
trend_rate = 0
tweet_rate = 0
openhours = []

file = open('responses.csv', 'a')
writer = csv.writer(file)

def makePrediction(placeID):
    try:
        global currentPrediction
        global day_forecast
        global place
        global google_ranking
        global weather_ranking
        global temps
        global forecast
        global chance_rain
        global trend_rate
        global tweet_rate
        global openhours

        [openhours, place] = getData.googleData(placeID)

        google_ranking = getData.getPopularTimes(placeID)  # returns [forecast, current]
        [feels_like, temps, cloud, forecast, chance_rain] = getData.getWeather()

        hour = datetime.datetime.now().hour

        name = getData.getPlaceName()
        name= name.split("-")[0]
        [week_trend, day_trend] = getData.getTrends(name)
        tweets = getData.getTweets(name)

        loaded_model = pickle.load(open('final_model.sav', 'rb'))

        complete_types = ['supermarket',
     'bakery',
     'grocery_or_supermarket',
     'food',
     'point_of_interest',
     'store',
     'establishment',
     'park',
     'tourist_attraction',
     'finance',
     'train_station',
     'transit_station',
     'hospital',
     'liquor_store',
     'health',
     'gas_station',
     'car_wash',
     'convenience_store',
     'pharmacy',
     'meal_delivery',
     'restaurant',
     'pet_store',
     'meal_takeaway',
     'natural_feature',
     'hardware_store',
     'home_goods_store',
     'bicycle_store',
     'car_repair',
     'clothing_store']
        encoded_types = [0]* len(complete_types)

        for i in range(len(complete_types)):
            if complete_types[i] in place:
                encoded_types[i] = 1

        # only write if we have legit data
        if google_ranking[1] != -1 and google_ranking[0] != [0]*24:
            writer.writerow([placeID, getData.getPlaceName(), hour, place, google_ranking[0][hour],
                         feels_like[hour], temps[hour], cloud[hour], forecast[hour], chance_rain[hour], week_trend, day_trend, tweets, google_ranking[1]])

        # deal with case google returned all 0s (i.e. no forecast)
        if google_ranking[0] == [0]*24:
            # google returned no data :(
            google_ranking[0] = [3,2,2,2,2,3,2,4,9,15,27,45,59,63,64,66,56,46,34,28,27,13,7,5] # calculated using mean for each time

        to_predict = []
        for i in range(24):
            to_predict.append([i, google_ranking[0][i], feels_like[i], temps[i], cloud[i], forecast[i], chance_rain[i], week_trend, day_trend, tweets
            ] + encoded_types)

        to_predict = pd.DataFrame.from_records(data=to_predict)

        output = loaded_model.predict(to_predict)

        day_forecast = output.tolist()

        opened = int(openhours[0])
        closed = int(openhours[1])
        print(opened, closed)
        if opened < closed:
            # normal shop open 9am close 6pm
            for i in range(0, opened):
                day_forecast[i] = 0
            for i in range(closed, 24):
                day_forecast[i] = 0
        else:
            # if time loops round e.g. open 9am to 3am
            for i in range(closed, opened):
                day_forecast[i] = 0

        if 'park' in place:
            # reduce the weighting slighly for parks
            day_forecast = [x * 0.7 for x in day_forecast]

        currentPrediction = day_forecast[datetime.datetime.now().hour]

        if google_ranking[1] != -1:
            if google_ranking[1] > currentPrediction + 10:
                currentPrediction = google_ranking[1] # we trust google...
    except:
        # ok something has gone wrong
        # this shouldnt have happened, but just incase lets return average values
        day_forecast = [3, 2, 2, 2, 2, 3, 2, 4, 9, 15, 27, 45, 59, 63, 64, 66, 56, 46, 34, 28, 27, 13, 7, 5]
        currentPrediction = day_forecast[datetime.datetime.now().hour]

def getCurrentPrediction():
    if currentPrediction > 70:
        return 4
    elif currentPrediction > 50:
        return 3
    elif currentPrediction > 25:
        return 2
    elif currentPrediction > 10:
        return 1
    else:
        return 0

def getQ():
    if  not getData.getIsOpen():
        return -1
    if 'supermarket' in place or 'store' in place or 'grocery_or_supermarket' in place or 'liquor_store' in place:
        if currentPrediction < 2:
            return 0
        elif currentPrediction < 5:
            return 1
        elif currentPrediction < 15:
            return 2
        elif currentPrediction < 30:
            return 3
        else:
            return 4
    return -1

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

def getOpenHours():
    return openhours

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
