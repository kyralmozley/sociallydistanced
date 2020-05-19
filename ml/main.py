#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Receive and generate requests to speak to the website
author: Kyra Mozley
'''
import csv
import json
import sys

import prediction

def reply(placeID):

    prediction.makePrediction(placeID)
    name = prediction.getPlaceName()
    rating = prediction.getCurrentPrediction()
    day_forecast = prediction.getDayForecast()
    open = prediction.getIsOpen()
    openhours = prediction.getOpenHours()
    queue = prediction.getQ()
    response = {
      'name' : name,
      'open' : open,
      'rating': rating,
      'day_forecast': day_forecast,
      'queue' : queue,
    'openhours' : openhours
    }

    r = json.dumps(response)
    print(r)
    return r




if __name__ == "__main__":
    reply(sys.argv[1])