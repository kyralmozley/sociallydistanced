import datetime

import getData

currentPrediction = 0
day_forecast = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

def makePrediction(placeID):
    global currentPrediction
    global day_forecast

    google_ranking = getData.getPopularTimes(placeID) # returns [forecast, current]
    [lat, long] = getData.googlePlaceIDtoLatLong(placeID)
    weather_ranking = getData.getWeather(lat, long)
    [temps, forecast, chance_rain] = weather_ranking

    combine = [a*b for a, b in zip(google_ranking[0], temps)]
    combine = [a*b for a,b in zip(combine, forecast)]
    combine = [a*b for a,b in zip(combine, chance_rain)]

    shift = datetime.date.today().weekday()
    currentPrediction = google_ranking[1] * temps[shift] * forecast[shift] * chance_rain[shift]
    day_forecast = combine

def getCurrentPrediction():
    return currentPrediction

def getDayForecast():
    return day_forecast