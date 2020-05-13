'''
Receive and generate requests to speak to the website
author: Kyra Mozley
'''
import requests
import json

import populartimes
import APIKey


def reply(lat, long, raiting):
    response = {
        'lat': lat,
        'long': long,
        'raiting': raiting
    }

    r = requests.post("http://localhost:80", json=response)
    print(r)

def getPopularTimes(placeID):
    api_key = APIKey.getGoogleAPIKey()
    populartimes.get_id(api_key, placeID)

reply(51.31575, 0.09271, 5)
getPopularTimes("ChIJhRoYKUkFdkgRDL20SU9sr9E")
'''
if __name__ == "__main__":
    reply()
'''