import datetime

import getData

currentPrediction = 0
day_forecast = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def makePrediction(placeID):
    global currentPrediction
    global day_forecast

    [lat, long, openhours] = getData.googleData(placeID)

    google_ranking = getData.getPopularTimes(placeID)  # returns [forecast, current]
    weather_ranking = getData.getWeather(lat, long)

    [temps, forecast, chance_rain] = weather_ranking
    combine = [a * b for a, b in zip(google_ranking[0], temps)]
    combine = [a * b for a, b in zip(combine, forecast)]
    combine = [a * b for a, b in zip(combine, chance_rain)]

    for x in range(0, int(openhours[0])):
        combine[x] = 0
    for x in range(int(openhours[1]), 24):
        combine[x] = 0

    shift = datetime.date.today().weekday()
    currentPrediction = google_ranking[1] * temps[shift] * forecast[shift] * chance_rain[shift]
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
    new = [i * 1.5 for i in day_forecast]
    return [int(i) for i in new]

def getPlaceName():
    return getData.getPlaceName()