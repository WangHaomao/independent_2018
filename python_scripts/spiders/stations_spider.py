# station name from
# https://www.travelchinaguide.com/cityguides/hongkong/transportation/subway.htm

# station information from
# wikipedia
import requests
from bs4 import BeautifulSoup
import pandas as pd

replace_dic = {
'https://en.wikipedia.org/wiki/Prince_Edward_station':'https://en.wikipedia.org/wiki/Prince_Edward_station_(MTR)',

'https://en.wikipedia.org/wiki/Olympic_station_(MTR)':'https://en.wikipedia.org/wiki/Olympic_station',

'https://en.wikipedia.org/wiki/Universtiy_station_(MTR)':'https://en.wikipedia.org/wiki/University_station_(MTR)',

'https://en.wikipedia.org/wiki/Yau_Ma_Tie_station':'https://en.wikipedia.org/wiki/Yau_Ma_Tei_station',

'https://en.wikipedia.org/wiki/Jordan_station_(MTR)':'https://en.wikipedia.org/wiki/Jordan_station',

'https://en.wikipedia.org/wiki/Tsui_Sha_Tsui_station':'https://en.wikipedia.org/wiki/Tsim_Sha_Tsui_station',

'https://en.wikipedia.org/wiki/HKU_station_(MTR)':'https://en.wikipedia.org/wiki/HKU_station',

'https://en.wikipedia.org/wiki/Whampoa_station_(MTR)':'https://en.wikipedia.org/wiki/Whampoa_station',

'https://en.wikipedia.org/wiki/Fanling_station_(MTR)':'https://en.wikipedia.org/wiki/Fanling_station',
}


def pre_data():
    data_folder = '../data/%s'

    with open(data_folder%'hk_mtr_stations.txt','r') as f:
        stations = f.readlines()
        stations = list(map(lambda x:x.replace('\n',''),stations))

    f.close()

    def make_url(station_name):
        base_url = 'https://en.wikipedia.org/wiki/%s_station'
        renamed = station_name.replace(' ','_')
        cnt = renamed.count('_')
        if(cnt == 0):
            station_url = (base_url % renamed) + '_(MTR)'
        else:
            station_url = base_url % renamed

        return station_url

    make_url(stations[0])
    stations_url_list = list(set(list(map(make_url,stations))))
    # pprint(stations_url_list)
    for i in range(len(stations_url_list)):
        if(stations_url_list[i] in replace_dic.keys()):
            stations_url_list[i] = replace_dic[
                stations_url_list[i]
            ]


    return stations,stations_url_list

def crawler(url):
    # url = 'https://en.wikipedia.org/wiki/Nam_Cheong_station'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'
        , 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }
    req = requests.get(url, headers=header)
    # 打开并读取url内信息
    html = req.text
    # 利用bs4库解析html
    soup = BeautifulSoup(html, "html.parser")
    latitude = soup.find('span',class_='latitude')
    longitude = soup.find('span',class_='longitude')
    if(latitude == None):
        # pass
        print(url)
    else:
        latitude = latitude.text.replace('″N','').replace('°','.').replace('′','')
        longitude = longitude.text.replace('″E','').replace('°','.').replace('′','')

        # print(latitude,longitude)


    return latitude,longitude


stations,stations_url = pre_data()

print(stations)

dd = {
    'station':[],
    'la':[],
    'lo':[]
}

for i in range(len(stations_url)):
    la,lo = crawler(stations_url[i])
    if(lo != None):
        dd['station'].append(stations[i])
        dd['la'].append(la)
        dd['lo'].append(lo)


tmp = pd.DataFrame.from_dict(dd)
tmp.to_csv('geo_MTRstation.csv',index=False)