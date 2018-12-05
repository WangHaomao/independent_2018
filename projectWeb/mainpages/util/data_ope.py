import pandas as pd
import numpy as np
import math

from pprint import pprint
data_folder = '../../../data/%s'
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


# print(list_name)


def search_min_dis(list_name,list_latln_str,places_lat,places_lng,column_name):
    total_num = len(list_name)
    places_tol = len(places_lat)
    res_dic = {
        'house_name': [],
        'lat_lon': [],
        column_name:[]
    }
    for i in range(total_num):
        la, ln = list_latln_str[i].split(',')
        lat = float(la)
        lng = float(ln)
        min_dis = np.inf
        for j in range(places_tol):
            p_lat = places_lat[j]
            p_lng = places_lng[j]

            min_dis = min(min_dis,get_distance(lat,lng,p_lat,p_lng))
            # print((lat, lng, p_lat, p_lng))
        res_dic['house_name'].append(list_name[i])
        res_dic['lat_lon'].append(list_latln_str[i])
        res_dic[column_name].append(min_dis)

    # pprint(res_dic)
    df_res = pd.DataFrame.from_dict(res_dic)
    return df_res

if __name__ == '__main__':


    geo_school = pd.read_csv(data_folder % 'add_res1203_shopping.csv')
    # MTR_lat = list(geo_MTRstation['la'].values)
    # MTR_lng = list(geo_MTRstation['lo'].values)

    school_lat = list(geo_school['shopping center'].str.split(',',expand = True)[0].astype('float64').values)
    school_lng = list(geo_school['shopping center'].str.split(',',expand = True)[1].astype('float64').values)

    df_es = pd.read_csv(data_folder % 'geo_file.csv')
    list_latln_str = list(df_es['lat/lng'])
    list_name = list(df_es['estateName'])

    # print(df_es)

    df_res = search_min_dis(list_name,list_latln_str,school_lat,school_lng,'mark_nearest')

    df_res.to_csv(data_folder % 'nearest_market.csv', index=False, encoding='utf-8-sig')
