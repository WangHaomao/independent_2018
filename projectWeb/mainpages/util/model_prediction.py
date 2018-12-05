import sys
sys.path.append('./util')
sys.path.append('..')
# from django.shortcuts import render
import pandas as pd
# Create your views here.
from googlemap_util import *
from pprint import pprint
import numpy as np
import datetime
from myconf import *
import myconf
import lightgbm as lgb
import mainpages
import os


def data_generate_pred(floor,areaSize,more_info):
    pth = os.path.dirname(mainpages.__file__)
    num_col = myconf.numerical_col
    date_col = myconf.date_col

    future_number = 6

    start_time = datetime.datetime.now()

    sixmonths = start_time + datetime.timedelta(days=365.25 / (12 / future_number))

    end_time = sixmonths.strftime('%Y-%m-%d')
    start_time = start_time.strftime('%Y-%m-%d')

    future_date = list(map(lambda x: x.strftime('%Y-%m-%d')
                           , list(pd.date_range(start=start_time, end=end_time, closed=None, freq='M'))
                           ))
    # print(future_date)

    pd_dict = {
        'floor': [float(floor)] * future_number,
        'dis_mtr': [float(more_info[1])] * future_number,
        'dis_school': [float(more_info[2])] * future_number,
        'dis_market': [float(more_info[3])] * future_number,
        'areaSize': [float(areaSize)] * future_number,
        'date': future_date
    }

    # pprint(pd_dict)

    test_data = pd.DataFrame.from_dict(pd_dict)
    test_data['date'] = pd.to_datetime(test_data['date'])
    test_data['year'] = test_data['date'].dt.year
    test_data['month'] = test_data['date'].dt.month
    test_data['day'] = test_data['date'].dt.day

    test_data = test_data.set_index('date')
    test_data = test_data.sort_index()
    test_data = test_data.reset_index()[num_col + date_col]

    # pd.Series.from_array()
    # print(test_data)
    mean, std, label_nor = get_normal()
    test_data[num_col] = (test_data[num_col] - mean) / std

    # print(test_data)

    gbm = lgb.Booster(model_file= pth+'/data/gbm_for_web.txt')
    # gbm = lgb.Booster(model_file='../../data/gbm_for_web.txt')

    pred = gbm.predict(test_data)
    pred = np.power(np.e, pred * 20)


    pred_mean = pred.mean().copy()
    pred = list(np.round(pred - pred.mean()))

    return pred, pred_mean

# if __name__ == '__main__':
#
#     house_info = '海都大廈,15,882'
#     name, floor, areaSize = house_info.split(',')
#     more_info = select_query(name)
#
#     data_generate(floor,areaSize,more_info)