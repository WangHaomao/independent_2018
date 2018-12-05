import googlemaps
from time import sleep
import pandas as pd
from tqdm import tqdm
import numpy as np
from datetime import datetime
from pprint import pprint
API_KEY = 'AIzaSyD9mARopyCHqRvb8_dTYlaPOo90fPwKvhw'
gmaps = googlemaps.Client(key=API_KEY)

# Geocoding an address
# geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

# Look up an address with reverse geocoding

# reverse_geocode_result = gmaps.reverse_geocode((22.3964,114.1095))

# Request directions via public transit
# now = datetime.now()
# directions_result = gmaps.directions("Sydney Town Hall",
#                                      "Parramatta, NSW",
#                                      mode="transit",
#                                      departure_time=now)


with open('../data/geo_file.txt','r') as f:
    read_f = f.readlines()
    list_latln_str = list(map(lambda x:str(x.replace('\n','').split('#')[1:][0]),read_f))
    list_name = list(map(lambda x:str(x.replace('\n','').split('#')[0]),read_f))
    # list_latln = list(map(lambda x:,read_f))
f.close()
# print(list_name)

total_num = len(list_name)

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
res_dic = {
    'house_name':[],
    'lat_lon':[],
}
add_info = {}
need_list = ['school']
# need_list = ['MTR', 'shopping center', 'school']
for i in tqdm(range(total_num)):
    la,ln  = list_latln_str[i].split(',')
    la = float(la)
    lo = float(ln)
    # print(la,lo)
    res_dic['house_name'].append(list_name[i])
    res_dic['lat_lon'].append(list_latln_str[i])


    target_geo = (la,lo)
    for nearby_name in need_list:
        search_keyword = nearby_name
        # res = gmaps.places_autocomplete_query(location=target_geo,input_text=search_keyword,radius=150)
        res = gmaps.places(location=target_geo,query=search_keyword,radius=500)['results']
        min_dis = np.inf
        min_la = 0
        min_ln = 0
        min_p_info = ''
        if (nearby_name not in add_info.keys()):
            add_info[nearby_name] = set()

        for each_p in res:
            p_lat = float(each_p['geometry']['location']['lat'])
            p_lng = float(each_p['geometry']['location']['lng'])


            add_info[nearby_name].add(str(p_lat)+','+str(p_lng))

            c_dis = get_distance(la,lo,p_lat,p_lng)
            if(c_dis < min_dis):
                min_dis = c_dis
                min_la = p_lat
                min_ln = p_lng
                min_p_info = each_p



        # pprint(min_p_info)
        # print(min_dis)
        # print(min_p_info)
        # print((la,lo,min_la,min_ln))

        if(nearby_name not in res_dic.keys()):
            res_dic[nearby_name] = []

        res_dic[nearby_name].append(min_dis)
    # print('finished at %d'%i)
    sleep(0.1)


for nearby_name in need_list:
    add_info[nearby_name] = list(add_info[nearby_name])



res = pd.DataFrame.from_dict(res_dic)
add_res = pd.DataFrame.from_dict(add_info)
# print(res.head(5))
res.to_csv('res1203_school.csv')
add_res.to_csv('add_res1203_school.csv')