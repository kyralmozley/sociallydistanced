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
    name = prediction.getPlaceName()
    rating = prediction.getCurrentPrediction()
    day_forecast = prediction.getDayForecast()

    response = {
        'name' : name,
        'rating': rating,
        'day_forecast': day_forecast,

    }

    r = json.dumps(response)
    print(r)
    return r




if __name__ == "__main__":
    #reply(sys.argv[1])

    #reply("ChIJL7CVDxgbdkgRnNimu0Q_Otc")
    #reply('ChIJ94YBg6obdkgR8kG7ia5Eu0g') # tesco metro kings x
    #reply('ChIJH5p8i1AbdkgRD01IW5aTTS4') # wework
    reply('ChIJxf19SeQadkgR_SGbcBrHVuk') #morrisons
    #reply('ChIJT__GzjB32EcRIAY_W2T_57I')
    #reply('ChIJ94YBg6obdkgR8kG7ia5Eu0g')
