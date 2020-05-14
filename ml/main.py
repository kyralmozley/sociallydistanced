'''
Receive and generate requests to speak to the website
author: Kyra Mozley
'''
import sys

import requests
import json

import prediction


def reply(placeID):
    prediction.makePrediction(placeID)
    rating = prediction.getCurrentPrediction()
    day_forecast = prediction.getDayForecast()
    #print(raiting, day_forecast)

    response = {
        'rating': rating,
        'day_forecast' : day_forecast
    }

    r = json.dumps(response)
    print(r)
    return r




if __name__ == "__main__":
    reply(sys.argv[1])
    # reply("ChIJL7CVDxgbdkgRnNimu0Q_Otc")

