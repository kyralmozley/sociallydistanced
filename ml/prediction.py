import datetime
import math

import getData

currentPrediction = 0
day_forecast = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def makePrediction(placeID):
    global currentPrediction
    global day_forecast

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

    if 'supermarket' in place or 'store' in place:
        weather_weighting = 1.5
    if 'park' in place:
        weather_weighting = 0.8

    name = getData.getPlaceName()
    name= name.split("-")[0]
    trend_weight = getData.getTrends(name)
    if trend_weight == 0:
        # assume something went wrong in finding the trend, do nothing
        trend_weight = 1
    else:
        trend_weight = math.log(trend_weight+1, 10)

    combine = [a * b for a, b in zip(combine, google_ranking[0])]
    combine = [i * weather_weighting * trend_weight for i in combine]


    for x in range(0, int(openhours[0])):
        combine[x] = 0
    if int(openhours[1]) != 0:
        for x in range(int(openhours[1]), 24):
            combine[x] = 0

    shift = datetime.date.today().weekday()
    currentPrediction = google_ranking[1] * temps[shift] * forecast[shift] * chance_rain[shift] * weather_weighting * trend_weight
    day_forecast = combine


def getCurrentPrediction():
    if currentPrediction > 40:
        return 4
    elif currentPrediction > 30:
        return 3
    elif currentPrediction > 20:
        return 2
    elif currentPrediction > 5:
        return 1
    else:
        return 0


def getDayForecast():
    return [int(i) for i in day_forecast]

def getPlaceName():
    return getData.getPlaceName()