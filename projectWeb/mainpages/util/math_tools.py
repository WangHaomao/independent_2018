import math
EARTH_RADIUS = 6378.137
def rad(d):
    return d * math.pi / 180.0

# KM
def get_distance(lat1,lng1,lat2,lng2):

    radLat1 = rad(lat1)
    radLat2 = rad(lat2)


    a = radLat1 - radLat2
    b = rad(lng1) - rad(lng2)

    s = 2.0 * math.asin(math.sqrt(math.pow(math.sin(a/2.0),2.0) +
            math.cos(radLat1)*math.cos(radLat2)*math.pow(math.sin(b/2.0),2.0)))
    s = s * EARTH_RADIUS

    s = round(s * 10000.0) / 10000.0

    return s

# print(get_distance(22.75424,112.76535 , 23.014171, 113.10111))