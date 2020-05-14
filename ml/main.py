'''
Receive and generate requests to speak to the website
author: Kyra Mozley
'''
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
    reply("ChIJL7CVDxgbdkgRnNimu0Q_Otc") #kings x
    #reply('ChIJObnMwj4bdkgRqYr_8ExiX4I') # tesco metro kings x
    #reply('ChIJH5p8i1AbdkgRD01IW5aTTS4') # wework
    #reply('ChIJxf19SeQadkgR_SGbcBrHVuk') #morrisons
    #reply('ChIJhRoYKUkFdkgRDL20SU9sr9E') #hyde
