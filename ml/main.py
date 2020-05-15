'''
Receive and generate requests to speak to the website
author: Kyra Mozley
'''
import csv
import json
import sys

import prediction

file = open('feedback.csv', 'a')
writer = csv.writer(file)

def reply(placeID):

    prediction.makePrediction(placeID)
    name = prediction.getPlaceName()
    rating = prediction.getCurrentPrediction()
    day_forecast = prediction.getDayForecast()
    open = prediction.getIsOpen()
    response = {
        'name' : name,
        'open' : open,
        'rating': rating,
        'day_forecast': day_forecast,
    }

    r = json.dumps(response)
    print(r)
    return r

def feedback(feedback, placeID):
    prediction.makePrediction(placeID)
    name = prediction.getPlaceName()
    rating = prediction.getCurrentPrediction()
    day_forecast = prediction.getDayForecast()
    open = prediction.getIsOpen()

    googleRanking = prediction.getGoogleRanking()
    weather = prediction.getWeatherRanking()
    temp = prediction.getTemps()
    forecast = prediction.getForecast()
    rain = prediction.getChanceRain()
    trend_rate = prediction.getTrendRate()
    tweet_rate = prediction.getTweetRate()
    response = [placeID, name, rating, day_forecast, open, googleRanking,
                weather, temp, forecast, rain, trend_rate, tweet_rate, feedback
                ]

    writer.writerow(response)
    return



if __name__ == "__main__":
    reply(sys.argv[1])

