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
    raiting = prediction.getCurrentPrediction()
    day_forecast = prediction.getDayForecast()
    print(raiting, day_forecast)

    response = {
        'raiting': raiting,
        'day_forecast' : day_forecast
    }

    r = requests.post("http://localhost:80", json=response)
    print(r)




if __name__ == "__main__":
    reply(sys.argv[1])
    # reply("ChIJL7CVDxgbdkgRnNimu0Q_Otc")

