import datetime

import getData

currentPrediction = 0
day_forecast = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def makePrediction(placeID):
    global currentPrediction
    global day_forecast

    google_ranking = getData.getPopularTimes(placeID)  # returns [forecast, current]
    [lat, long] = getData.googlePlaceIDtoLatLong(placeID)
    weather_ranking = getData.getWeather(lat, long)
    [temps, forecast, chance_rain] = weather_ranking

    combine = [a * b for a, b in zip(google_ranking[0], temps)]
    combine = [a * b for a, b in zip(combine, forecast)]
    combine = [a * b for a, b in zip(combine, chance_rain)]

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
    elif currentPrediction > 10:
        return 1
    else:
        return 0


def getDayForecast():
    forecast = []
    for item in day_forecast:
        if item > 40:
            forecast.append(4)
        elif item > 30:
            forecast.append(3)
        elif item > 20:
            forecast.append(2)
        elif item > 10:
            forecast.append(1)
        else:
            forecast.append(0)
    return forecast
