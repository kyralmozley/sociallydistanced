import pprint

import populartimes
import APIKey
import datetime

import requests

'''
Map the weather response code to the probability of going out
Note: this is currently done purely on my judgement 
1 = I'm going out to have a BBQ and beer right now
0.1 = not going outside staying in bed 
(0.1 rather than 0 for smoothing reasons)
'''
weather_dictionary = {
    200: 0.3,  # Thunderstorm with light rain
    201: 0.3,  # Thunderstorm with rain
    202: 0.1,  # Thunderstorm with heavy rain
    230: 0.3,  # Thunderstorm  with light drizzle
    231: 0.2,  # Thunderstorm with drizzle
    232: 0.1,  # Thunderstorm with heavy drizzle
    233: 0.1,  # Thunderstorm with hail
    300: 0.7,  # light drizzle
    301: 0.6,  # drizzle
    500: 0.6,  # light rain
    501: 0.5,  # moderate rain
    502: 0.3,  # heavy rain
    511: 0.1,  # freezing rain
    520: 0.6,  # light shower rain
    521: 0.5,  # shower rain
    522: 0.2,  # heay shower rain
    600: 0.2,  # light snow
    601: 0.2,  # snow
    602: 0.1,  # heavy snow
    610: 0.1,  # snow rain
    611: 0.2,  # sleet
    612: 0.1,  # heavy sleet
    621: 0.1,  # snow shower
    622: 0.1,  # heavy snow shower
    623: 0.3,  # flurries
    700: 0.7,  # mist
    711: 0.7,  # smoke
    721: 0.7,  # haaze
    731: 0.7,  # sand/dust
    741: 0.7,  # fog
    751: 0.5,  # freezing fog
    800: 1.0,  # clear sky
    801: 0.95,  # few clouds
    802: 0.9,  # scattered clouds
    803: 0.8,  # broken clouds,
    804: 0.75,  # overcas clouds,
    900: 0.4  # unknown precip
}

def googleLatLongtoPlaceID(lat, long):
    api_key = APIKey.getGoogleAPIKey()
    url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng=' + str(lat) + ',' + str(long) + '&key=' + api_key
    google_data = requests.get(url).json()
    return google_data['results'][0]['place_id']

def googlePlaceIDtoLatLong(placeID):
    api_key = APIKey.getGoogleAPIKey()
    url = 'https://maps.googleapis.com/maps/api/geocode/json?place_id=' + placeID + '&key=' + api_key
    google_data = requests.get(url).json()

    latlong = google_data['results'][0]['geometry']['location']
    return [latlong['lat'], latlong['lng']]


def getPopularTimes(placeID):
    current_estimate = 0
    forecast = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    api_key = APIKey.getGoogleAPIKey()

    pop_times = populartimes.get_id(api_key, placeID)
    #pprint.pprint(pop_times)

    if 'populartimes' in pop_times:
        # return the prediction for today's forecast courtesy of Google Maps
        forecast = pop_times['populartimes'][datetime.date.today().weekday()].get('data')
    else:
        url = 'https://maps.googleapis.com/maps/api/place/details/json?place_id='+ placeID + '&key=' + api_key
        get_data = requests.get(url).json()
        #pprint.pprint(get_data)

    if 'current_popularity' in pop_times:
        current_estimate = pop_times['current_popularity']
        #print(current_estimate)

    elif 'populartimes' in pop_times:
        current_estimate = forecast[datetime.datetime.now().hour]

    return [forecast, current_estimate]


def getWeather(lat, lon):
    api_key = APIKey.getWeatherKey()
    url = 'https://api.weatherbit.io/v2.0/forecast/hourly?lat=' + str(lat) + '&lon=' + str(
        lon) + '&key=' + api_key + '&hours=24'
    weather_data = requests.get(url).json()

    temps = []
    forecast = []
    chanceRain = []

    for hour in weather_data['data']:
        temps.append((hour['app_temp'] + 3) / (31)) # normalising, 34 highest, -3 lowest
        get_forecast = hour['weather']['code']
        forecast.append(weather_dictionary[get_forecast])
        chanceRain.append(1 - (hour['precip'] / 210)) #normalising, 210 highest recorded value this year

    # need to rotate arrays so midnight-midnight
    slice = datetime.datetime.now().hour
    temps = temps[slice:] + temps[:slice]
    forecast = forecast[slice:] + forecast[:slice]
    chanceRain = chanceRain[slice:] + chanceRain[:slice]

    return [temps, forecast, chanceRain]
'''
def getopeningtimes():
    response = '{'address': '90 York Way, London N1 9AG, UK',
 'coordinates': {'lat': 51.5349492, 'lng': -0.121605},
 'id': 'ChIJH5p8i1AbdkgRD01IW5aTTS4',
 'international_phone_number': '+44 20 3695 7895',
 'name': 'WeWork Kings Place',
 'rating': 4.5,
 'rating_n': 1403,
 'types': ['real_estate_agency', 'point_of_interest', 'establishment']}
{'html_attributions': [],
 'result': {'address_components': [{'long_name': '90',
                                    'short_name': '90',
                                    'types': ['street_number']},
                                   {'long_name': 'York Way',
                                    'short_name': 'York Way',
                                    'types': ['route']},
                                   {'long_name': 'London',
                                    'short_name': 'London',
                                    'types': ['postal_town']},
                                   {'long_name': 'Greater London',
                                    'short_name': 'Greater London',
                                    'types': ['administrative_area_level_2',
                                              'political']},
                                   {'long_name': 'England',
                                    'short_name': 'England',
                                    'types': ['administrative_area_level_1',
                                              'political']},
                                   {'long_name': 'United Kingdom',
                                    'short_name': 'GB',
                                    'types': ['country', 'political']},
                                   {'long_name': 'N1 9AG',
                                    'short_name': 'N1 9AG',
                                    'types': ['postal_code']}],
            'adr_address': '<span class="street-address">90 York Way</span>, '
                           '<span class="locality">London</span> <span '
                           'class="postal-code">N1 9AG</span>, <span '
                           'class="country-name">UK</span>',
            'business_status': 'OPERATIONAL',
            'formatted_address': '90 York Way, London N1 9AG, UK',
            'formatted_phone_number': '020 3695 7895',
            'geometry': {'location': {'lat': 51.5349492, 'lng': -0.121605},
                         'viewport': {'northeast': {'lat': 51.5362950802915,
                                                    'lng': -0.120599469708498},
                                      'southwest': {'lat': 51.5335971197085,
                                                    'lng': -0.123297430291502}}},
            'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/generic_business-71.png',
            'id': 'ad0a128e53fdb426413fc95b5ee62baee9f9735b',
            'international_phone_number': '+44 20 3695 7895',
            'name': 'WeWork Kings Place',
            'opening_hours': {'open_now': True,
                              'periods': [{'close': {'day': 1, 'time': '1800'},
                                           'open': {'day': 1, 'time': '0900'}},
                                          {'close': {'day': 2, 'time': '1800'},
                                           'open': {'day': 2, 'time': '0900'}},
                                          {'close': {'day': 3, 'time': '1800'},
                                           'open': {'day': 3, 'time': '0900'}},
                                          {'close': {'day': 4, 'time': '1800'},
                                           'open': {'day': 4, 'time': '0900'}},
                                          {'close': {'day': 5, 'time': '1800'},
                                           'open': {'day': 5, 'time': '0900'}}],
                              'weekday_text': ['Monday: 9:00 AM – 6:00 PM',
                                               'Tuesday: 9:00 AM – 6:00 PM',
                                               'Wednesday: 9:00 AM – 6:00 PM',
                                               'Thursday: 9:00 AM – 6:00 PM',
                                               'Friday: 9:00 AM – 6:00 PM',
                                               'Saturday: Closed',
                                               'Sunday: Closed']},
            'photos': [{'height': 426,
                        'html_attributions': ['<a '
                                              'href="https://maps.google.com/maps/contrib/115387984084454908364">WeWork '
                                              'Kings Place</a>'],
                        'photo_reference': 'CmRaAAAAQM6iLAdyRg34pBI5rYQUg74ULXvVv_Zmvro_V4DrNoLBSEThFTN-SSqBbCyQekd-LXWmnj1lGOdBiN7SXqepcviX77V1AAkUj__zpXuYJxXXVnPJm4NajjbLYvYOlpmwEhBLBkMq_fR3xwl_56XwsHgyGhQJybjhbPPGspiawLI-Uikm4BMuwg',
                        'width': 758},
                       {'height': 3008,
                        'html_attributions': ['<a '
                                              'href="https://maps.google.com/maps/contrib/114416295367143707423">Drago '
                                              'Indjic</a>'],
                        'photo_reference': 'CmRaAAAAjG_WHj8P4LsRGvzOCDLEoYDyXNWi8w3H-9RPqxcMPlTeHbjzgxmAfUy4mnNnYfZIHaY44U0d9REvqT8e0ELTQQ8NvSYiUjzcKCruCmla0RHjarl8EI6M3lPqzHvtgYVYEhDvvwSHhFMo8sDnDxE_eEZoGhT4QKvAdeskXGibgZ8iKD10Z55SWg',
                        'width': 4016},
                       {'height': 3024,
                        'html_attributions': ['<a '
                                              'href="https://maps.google.com/maps/contrib/108693321432222898191">Yonatan '
                                              'Matalon</a>'],
                        'photo_reference': 'CmRaAAAAEynk05ugcuaK5YZyXL7jp0Y8SIpWmPCibki9-njPuypfa-4ufizVRtyfBHdQ-TBh1OcWJBdbk-3zEcvZ-idLldx8lgH7EcICy0IsujeZLApdlnV6gQ0CJ6oGpkcTHdYLEhAyh7OjIb1_UAKaEu252YBeGhS651o1eywVNhfZMp4nCBK0qbB-AQ',
                        'width': 4032},
                       {'height': 3024,
                        'html_attributions': ['<a '
                                              'href="https://maps.google.com/maps/contrib/100655811043320324901">Kevin '
                                              'Wallis-Eade</a>'],
                        'photo_reference': 'CmRaAAAA2YitOTEX4Stm2Rye-pO3opX99T671ROUp9PN2pBF7XsaMrO7p8HHNPGSXr_bo1fvG6kka4Ft1JWzPt9_dezBWKV1N8ge-sM2ig5yOQQf4x0yFhpHoGMEDBj_IW7gZIcMEhBtMWPL8GNcD8YSwYGEpXl-GhQQT-br6S0pc1ifuPxCtnS0AUv0sg',
                        'width': 4032},
                       {'height': 1044,
                        'html_attributions': ['<a '
                                              'href="https://maps.google.com/maps/contrib/115387984084454908364">WeWork '
                                              'Kings Place</a>'],
                        'photo_reference': 'CmRaAAAAkCS-D5SuNtwdSIytjhRQhOPcxpeCsAS4SdPQ9i_dQkN5XnEsD2hNrsq99Zja26iR8Vr4jXgJhB_E3Kvnf09T5pTaUnNPfDodxs0kHXgUe2mgla20R_eCOMGWhEq9Xp0EEhBSNu0GocH0Y-Bb4S5cA5zDGhTm5HAwPSyWrmfgjmNgOpZVNAmLUw',
                        'width': 1566},
                       {'height': 2322,
                        'html_attributions': ['<a '
                                              'href="https://maps.google.com/maps/contrib/115380712751181019588">Mrs '
                                              'Mimi</a>'],
                        'photo_reference': 'CmRaAAAAcjhiuHKWZSkanWlCroWFqFHtjjKA1Q7bJje8utravxJJNhoco_v3CNrVEfNXvy1npEV2MgP7Y2-QDVC50qIYVFxasW6FzckmXt9T2dYcoEPw2He1PTCGiqpIbn8LK8LzEhD3yeXLkKt41E0SyfKlRO2sGhRgwNOPMlj0VuJowQZAfbPTPbwVfA',
                        'width': 4128},
                       {'height': 1440,
                        'html_attributions': ['<a '
                                              'href="https://maps.google.com/maps/contrib/110918639559378001957">Alice '
                                              'Martin</a>'],
                        'photo_reference': 'CmRaAAAARlKavJKSggVCj8cJZPWrkcg8pj2Qq0oZbW47sh1xIqAknzaTwxz3KGY8KCKxZH_nJG-e3NVXHcUN5MxOMuXRlq2Nj-tXyF2RQrTBFcT8pAi8hfPhgEXfV92P_Gd0UEybEhC3KMyRGrIqLxmjt8uaNbO9GhQfMKhhngA1zAEMmVSjNDCFf5vVBw',
                        'width': 2560},
                       {'height': 3024,
                        'html_attributions': ['<a '
                                              'href="https://maps.google.com/maps/contrib/101597484841229205770">Flo '
                                              'Yeow</a>'],
                        'photo_reference': 'CmRaAAAA604weUTFmPpeqx8HI7NHcLIoorfAtlagmDPvMbyo3DbxIbt8E8BLdjchDnuLidpuf786QeZFgNSq93e1VdhiyPyrrX1wmW8jYzA5sCJMgU6OCl_eF6StUSrkCk14neLyEhBZYSKHkonwrGk3Jzskt9PBGhQt5e-lXI-HdGxLPp8ZNEyqpf7XQg',
                        'width': 4032},
                       {'height': 3024,
                        'html_attributions': ['<a '
                                              'href="https://maps.google.com/maps/contrib/104014608618157234252">Amancio '
                                              'Bouza</a>'],
                        'photo_reference': 'CmRaAAAAemEI7VSgJhQAMIvyckydUWNqV2V9Xz8xgNdhsBGPPflEWIC0903ykT7x6N-0ij1P23tovBlLLMr3sJjk1d5pis-oKUeiSDyNpsoLsZRPUbCOjK1G5J1dDHkhzUOyHNXWEhALoCLCJkVI_y9rTY5bJ7lxGhSXwwGbeLPfODCIfl76yMp543EiMg',
                        'width': 4032},
                       {'height': 1824,
                        'html_attributions': ['<a '
                                              'href="https://maps.google.com/maps/contrib/111192666634366838553">Michele '
                                              'Scalisi</a>'],
                        'photo_reference': 'CmRaAAAAUUfA-rOSGLygFJUnqMhTU3BxZhoskCv7rJwgNSYf6_6Uopc_T_sUG-3rGsKYXrsXjUjLeVJdkairLAYXWy7w_XrYI_E_VezwheSTjgi9vgmU9g2zw3qRXy-6qCz5VI7MEhB6tARD_UAfjFIURoyIJAuHGhTe_GP-nK4zoyX-IZ76Pf72ShB42Q',
                        'width': 3648}],
            'place_id': 'ChIJH5p8i1AbdkgRD01IW5aTTS4',
            'plus_code': {'compound_code': 'GVMH+X9 London, United Kingdom',
                          'global_code': '9C3XGVMH+X9'},
            'rating': 4.5,
            'reference': 'ChIJH5p8i1AbdkgRD01IW5aTTS4',
            'reviews': [{'author_name': 'Dogs are great',
                         'author_url': 'https://www.google.com/maps/contrib/107752453883064212474/reviews',
                         'language': 'en',
                         'profile_photo_url': 'https://lh5.ggpht.com/-K1i4XwPNjnA/AAAAAAAAAAI/AAAAAAAAAAA/ZP3qhy7XqBc/s128-c0x00000000-cc-rp-mo-ba3/photo.jpg',
                         'rating': 5,
                         'relative_time_description': '3 months ago',
                         'text': 'Very beautiful venue. It has nice acoustics '
                                 'and atmosphere, quite small halls and lovely '
                                 'staff. The bar serves drinks at slightly '
                                 'expensive prices, but it is central London, '
                                 "so that's kind of normal. The events on "
                                 'there are always interesting, and have good '
                                 'themes to them. Overall a very good place to '
                                 'watch concerts, and to just hang out with '
                                 'family and friends.',
                         'time': 1581256726},
                        {'author_name': 'mich',
                         'author_url': 'https://www.google.com/maps/contrib/104923753888052949946/reviews',
                         'language': 'en',
                         'profile_photo_url': 'https://lh6.ggpht.com/--uCa2bh7R0I/AAAAAAAAAAI/AAAAAAAAAAA/xTnkqka9Geg/s128-c0x00000000-cc-rp-mo/photo.jpg',
                         'rating': 5,
                         'relative_time_description': '2 months ago',
                         'text': 'Absolutely love this venue although it can '
                                 "be tricky to find. It's across the road from "
                                 'the trendy Granary Square & is a great '
                                 'little hideaway. Comfortable leather sofas '
                                 'in the main foyer area with a cafe serving '
                                 "delicious cakes and hot food. There's also a "
                                 'bar with attached restaurant and in the '
                                 "summer, it's a pleasure to sit in deckchairs "
                                 'overlooking the canal. Downstairs there are '
                                 'two concert halls with very reasonably '
                                 'priced tickets and friendly staff: Hall 1 in '
                                 'particular has very comfortable seating with '
                                 'great views to the stage & a variety of '
                                 'performances - classical music, Guardian '
                                 'lectures, poetry, folk. You name it, they do '
                                 'it. But why oh why is the exterior of the '
                                 "building so discrete?  It's impossible to "
                                 'find and looks like an office block from the '
                                 'outside. Surely a nicely lit Kings Place '
                                 'sign at the top would help it to stand out '
                                 "from the crowd?  Come on King's Place, don't "
                                 'be so shy!',
                         'time': 1582766203},
                        {'author_name': 'Deborah Hiller',
                         'author_url': 'https://www.google.com/maps/contrib/106400827448612596064/reviews',
                         'language': 'en',
                         'profile_photo_url': 'https://lh5.ggpht.com/-B001oQpqvTc/AAAAAAAAAAI/AAAAAAAAAAA/ujuO0ikVA5U/s128-c0x00000000-cc-rp-mo-ba5/photo.jpg',
                         'rating': 4,
                         'relative_time_description': '6 months ago',
                         'text': 'Lovely little venue. We saw Focus who were '
                                 'brilliant. The sound was great. The food was '
                                 'good, albeit that the deserts were delayed '
                                 'and the ice-cream was a bit mean! Still, we '
                                 "weren't there for the food! We had a lovely "
                                 'evening, all in all.',
                         'time': 1573067772},
                        {'author_name': 'Campbell White',
                         'author_url': 'https://www.google.com/maps/contrib/102170540174356915783/reviews',
                         'language': 'en',
                         'profile_photo_url': 'https://lh4.ggpht.com/-JDu6g5qo08c/AAAAAAAAAAI/AAAAAAAAAAA/RWyRoFcJ-rI/s128-c0x00000000-cc-rp-mo-ba6/photo.jpg',
                         'rating': 4,
                         'relative_time_description': '4 months ago',
                         'text': 'Small modern concert venue with good '
                                 'acoustics and clear views of the stage from '
                                 'the main seating area.\n'
                                 '\n'
                                 'Upper balcony seating also provides good '
                                 'views.\n'
                                 '\n'
                                 'Large bar area just outside entrance to '
                                 'concert hall with a few seats.\n'
                                 '\n'
                                 'Cafeteria on the main entrance floor '
                                 'offering good value snacks/ meals.\n'
                                 '\n'
                                 'Short walk from Kings Cross tube station.',
                         'time': 1576693800},
                        {'author_name': 'Clifford Kunze',
                         'author_url': 'https://www.google.com/maps/contrib/117943423512670697984/reviews',
                         'language': 'en',
                         'profile_photo_url': 'https://lh4.ggpht.com/-1LiTdTM2wAI/AAAAAAAAAAI/AAAAAAAAAAA/nOIghK8zvYE/s128-c0x00000000-cc-rp-mo/photo.jpg',
                         'rating': 5,
                         'relative_time_description': '4 months ago',
                         'text': 'Love the architecture. The venue was superb, '
                                 'cheerful staff, great acoustic. Great '
                                 'comfortable place with fantastic ambitious '
                                 'programming. Great food & drink.',
                         'time': 1577126799}],
            'scope': 'GOOGLE',
            'types': ['real_estate_agency',
                      'point_of_interest',
                      'establishment'],
            'url': 'https://maps.google.com/?cid=3336485172937248015',
            'user_ratings_total': 1403,
            'utc_offset': 60,
            'vicinity': '90 York Way, London',
            'website': 'https://www.wework.com/buildings/kings-place--london?utm_source=Google&utm_campaign=Organic&utm_medium=Listings'},
 'status': 'OK'}'

'''