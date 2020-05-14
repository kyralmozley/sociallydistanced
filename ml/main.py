'''
Receive and generate requests to speak to the website
author: Kyra Mozley
'''
import json
import sys

import prediction


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




if __name__ == "__main__":
    reply(sys.argv[1])

