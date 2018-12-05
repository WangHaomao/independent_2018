# -*- coding:utf-8 -*-
import pymysql
import pandas as pd
data_folder = '../../../data/%s'

def database_conn():
    conn = pymysql.connect(host='localhost', user='root', passwd='123456', db='2018_HKUST_IP', port=3306,
                           charset="utf8")
    return conn

def init_insert_query():
    conn = database_conn()
    near_mtr = pd.read_csv(data_folder % 'nearest_mtr.csv')
    near_school = pd.read_csv(data_folder % 'nearest_school.csv')
    near_market = pd.read_csv(data_folder % 'nearest_market.csv')

    mtr_list = list(near_mtr['MTR_nearest'].values)
    school_list = list(near_school['school_nearest'].values)
    market_list = list(near_market['mark_nearest'].values)
    estate_name_list = list(near_mtr['house_name'].values)
    len_estate_name = len(estate_name_list)

    query = """INSERT INTO nearby_info(estate_name,mtr, school, market) VALUES ("{0}",{1}, {2}, {3})"""

    cur = conn.cursor()
    insert_set = set()
    for i in range(len_estate_name):
        if(estate_name_list[i] in insert_set): continue
        sql = query.format(estate_name_list[i],
                      str(mtr_list[i]),
                      str(school_list[i]),
                      str(market_list[i]))
        # print(sql)
        # break

        insert_set.add(estate_name_list[i])
        try:
            cur.execute(sql)
        except:
            print(estate_name_list[i])

    conn.commit()
    conn.close()

def insert_one_recoder_query(insert_data):
    conn = database_conn()

    query = """INSERT INTO nearby_info(estate_name,mtr, school, market) VALUES ("{0}",{1}, {2}, {3})"""

    cur = conn.cursor()
    insert_set = set()

    sql = query.format(insert_data[0],
                       str(insert_data[1]),
                       str(insert_data[2]),
                       str(insert_data[3]))

    try:
        cur.execute(sql)
    except:
        print(insert_data)

    conn.commit()
    conn.close()

def select_query(estate_name):
    conn = database_conn()

    cur=conn.cursor()
    query = 'SELECT * FROM nearby_info where estate_name like "%{0}%"'.format(estate_name)

    # print(query)
    # num = []
    cur.execute(query)

    data = cur.fetchone()

    conn.close()

    return data





if __name__ == '__main__':
    # print cdc_query(u"北京")
    # init_insert_query()
    select_query('s')