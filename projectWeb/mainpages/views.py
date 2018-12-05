import sys
sys.path.append('./util')
sys.path.append('.')
# from django.shortcuts import render
import pandas as pd
# Create your views here.
from mysql_ope import *
from googlemap_util import *
from pprint import pprint
import numpy as np
import datetime
from myconf import *
from model_prediction import *
import lightgbm as lgb
from django.shortcuts import render, HttpResponse
from functools import reduce
from django.http import HttpResponseRedirect
from django.core.files.storage import default_storage

def index(request):
    return render(request,'backend/test.html')
def single_prediction(request):
    return render(request,'backend/single_prediction.html')
def batch_prediction(request):
    return render(request,'backend/batch_prediction.html')
def model_selection(request):
    return render(request,'backend/model_selection.html')
def reBuild_model(request):
    return render(request,'backend/reBuild_model.html')

# action

def single_action(request):
    house_info = request.POST.get('house_info')

    name,floor,areaSize = house_info.split(',')
    more_info = select_query(name)
    if(more_info == None):
        more_info = get_nearest
        insert_one_recoder_query(more_info)

    pred_res,pred_mean = data_generate_pred(floor,areaSize,more_info)
    data_pred = 'data : [' + reduce(lambda x,y:str(x)+','+str(y),pred_res) + '],'
    # {'data_pred': data_pred}
    return render(request, 'backend/single_res.html',
                  {'data_pred': data_pred,'es_name':name,'pred_mean':np.round(pred_mean,2)})

def map_action(request):
    estate_info = request.POST.get('estate_info')
    search_keyword = request.POST.get('search_keyword')
    if(search_keyword == None or search_keyword == ''):
        search_keyword = 'MTR stations'
    # name, floor, areaSize = house_info.split(',')
    name = estate_info

    lat,lng = get_geo(name)
    return render(request, 'backend/estate_nearby.html',
                  {'estate_name': name,
                   'lat':lat,
                   'lng':lng,
                   'search_keyword':search_keyword,
                   'estate_info':estate_info})