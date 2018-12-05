import googlemaps
import numpy as np
import math
EARTH_RADIUS = 6378.137
def rad(d):
    return d * math.pi / 180.0

# KM
def get_distance(lat1,lng1,lat2,lng2):

    radLat1 = rad(lat1)
    radLat2 = rad(lat2)
    a = radLat1 - radLat2;
    b = rad(lng1) - rad(lng2)

    s = 2.0 * math.asin(math.sqrt(math.pow(math.sin(a/2.0),2.0) +
            math.cos(radLat1)*math.cos(radLat2)*math.pow(math.sin(b/2.0),2.0)))
    s = s * EARTH_RADIUS

    s = round(s * 10000.0) / 10000.0

    return s
def get_geo(search_keyword):

    API_KEY = 'AIzaSyD9mARopyCHqRvb8_dTYlaPOo90fPwKvhw'
    gmaps = googlemaps.Client(key=API_KEY)

    GEO_LOCATION = (22.3964, 114.1095)


    res = gmaps.places(location=GEO_LOCATION, query=search_keyword, radius=150)['results']

    try:
        lat = res[0]['geometry']['location']['lat']
        lng = res[0]['geometry']['location']['lng']
    except:
        lat = None
        lng = None

    return lat,lng

# print(get_geo('海都大厦'))
def get_nearest(search_keyword):

    API_KEY = 'AIzaSyD9mARopyCHqRvb8_dTYlaPOo90fPwKvhw'
    gmaps = googlemaps.Client(key=API_KEY)

    GEO_LOCATION = (22.3964, 114.1095)


    res = gmaps.places(location=GEO_LOCATION, query=search_keyword, radius=150)['results']

    try:
        lat = res[0]['geometry']['location']['lat']
        lng = res[0]['geometry']['location']['lng']
    except:
        return None

    GEO_LOCATION = (lat,lng)
    rrr_dic = {}
    for n_info in ['MTR', 'school','shopping center']:

        res = gmaps.places(location=GEO_LOCATION, query=n_info, radius=150)['results']

        min_dis = np.inf
        for each_p in res:
            p_lat = float(each_p['geometry']['location']['lat'])
            p_lng = float(each_p['geometry']['location']['lng'])

            c_dis = get_distance(lat,lng,p_lat,p_lng)
            if(c_dis < min_dis):
                min_dis = c_dis

        rrr_dic[n_info] = min_dis

    return (
        search_keyword,
        rrr_dic['MTR'],
        rrr_dic['school'],
        rrr_dic['shopping center']
    )