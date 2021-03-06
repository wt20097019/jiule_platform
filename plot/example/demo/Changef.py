# coding=utf8

import pandas as pd
import numpy as np
import time



"""时间转换为24小时制上，丢弃日期"""
def Str_Change_Time(N):
    def Str_Change_time_str(strchange):
        time_pro = time.localtime(strchange)
        if N == 0:
            data_value = time_pro[3] + int(time_pro[4]/10)/6
            data_value = float('%.2f' % data_value)
        elif N == 1:
            data_value = time_pro[3] + int(time_pro[4] / 10) / 6 + 0.08
            data_value = float('%.2f' % data_value)
        elif N == 2:
            data_value = time_pro[3] + int(time_pro[4]/10)/6
            data_value = float('%.1f' % data_value)
        elif N == 3:
            data_value = time_pro[3]
        return data_value
    return Str_Change_time_str


"""字符串转换到数字"""
def Str_Chage_N(n):
    def str_change_in(strchange):
        if n >= 16:
            coe = 2
        else:
            coe = 4
        if len(strchange) >= n + 2:
            data_value = int(strchange[n:n + 2], 16) * coe
        else:
            data_value = 0
        if strchange[0:6] == '120816' and n == 14:
            data_value = 1
        return data_value

    return str_change_in

def Str_Chnage_data(N):
    def Str_Change(strchange):
        if N == 0:
            data_value = int(strchange[0:2], 16) * 8
        elif N == 1:
            data_value = int(strchange[2:4], 16) * 8
        elif N == 2:
            data_value = int(strchange[4:6], 16) * 8
        elif N == 3:
            data_value = int(strchange[21], 16) & 1
        elif N ==4:
            data_value = int(strchange[22:24], 16) * 256 + int(strchange[24:26], 16)
        elif N == 5:
            data_value = int(strchange[22:24], 16)
        elif N == 6:
            data_value = int(strchange[6:8], 16) * 4
        elif N == 7:
            data_value = int(strchange[8], 16) + 1
        elif N == 8:
            data_value = int(int(strchange[8:10], 16) / 16) + 1
            if data_value == 8:
                data_value = 7
            if int(strchange[33], 16) == 0:
                data_value = 0
        elif N == 9:
            data_value = int(strchange[11], 16) + 0.1
        return data_value
    return Str_Change


"""提取字符串，存到dataFrame结构中"""
def Change_Str_Data(da):
    length = len(da)

    if length > 1:
        temp1 = pd.DataFrame(np.arange(length), columns=['timestamp'])
        temp1['wear_data'] = da['wear_data'].map(Str_Chage_N(14))
        temp2 = pd.DataFrame(np.arange(length), columns=['timestamp'])
        temp2['wear_data'] = da['wear_data'].map(Str_Chage_N(12))

        temp1['timestamp'] = da['timestamp'].map(Str_Change_Time(2))
        temp2['timestamp'] = da['timestamp'].map(Str_Change_Time(2))

        temp1['timestamps'] = da['timestamp'].map(Str_Change_Time(0))
        temp2['timestamps'] = da['timestamp'].map(Str_Change_Time(1))

        temp1['Activity'] = da['wear_data'].map(Str_Chage_N(18))
        temp2['Activity'] = da['wear_data'].map(Str_Chage_N(16))

        temp1['movement'] = da['wear_data'].map(Str_Chnage_data(4))
        temp2['movement'] = da['wear_data'].map(Str_Chnage_data(4))

        temp1['channel1'] = da['wear_data'].map(Str_Chnage_data(0))
        temp2['channel1'] = da['wear_data'].map(Str_Chnage_data(0))

        temp1['channel2'] = da['wear_data'].map(Str_Chnage_data(1))
        temp2['channel2'] = da['wear_data'].map(Str_Chnage_data(1))

        temp1['channel3'] = da['wear_data'].map(Str_Chnage_data(2))
        temp2['channel3'] = da['wear_data'].map(Str_Chnage_data(2))

        temp1['Charge'] = da['wear_data'].map(Str_Chnage_data(3))
        temp2['Charge'] = da['wear_data'].map(Str_Chnage_data(3))

        temp1['Wear_type'] = da['wear_type']
        temp2['Wear_type'] = da['wear_type']

        temp1['activity'] = da['activity']
        temp2['activity'] = da['activity']

        temp3 = pd.merge(temp1, temp2, how='outer')
        temp3 = temp3.sort_values(axis=0, ascending=True, by='timestamp')
        temp3.index = np.arange(len(temp3))
    else:
        temp3 = []
    return temp3


"""计算每次血氧计算耗时"""
def time_cost(mh):
    date = time.strptime(mh, '%Y-%m-%d %H:%M:%S')
    hh = (date[4] % 10) * 60 + date[5]
    if hh >= 90:
        hh = 90
    return hh


def num(str1):
    str2 = str1[1:6]
    num_cnt = int(str2)
    return num_cnt



def abs_diff(num):
    if num <= 0 :
        num = 0
    else:
        num = num
    return num



def Bad_output(input):
    if input == 220:
        output = 20
    elif input == 217:
        output = 15
    else:
        output = 0
    return output


def Time_get(N):
    def  Choose(strdata):
        timeArray = time.strptime(strdata, "%Y-%m-%d %H:%M:%S")
        if N == 0:
            date = timeArray[2]
        else:
            date = timeArray[3]
        return date
    return Choose



def Data_martix(da):

    length1 = len(da)
    if length1 > 1:
        da.index = np.arange(length1)
        temp_spo2 = pd.DataFrame(np.arange(length1), columns=['spo2'])
        temp_spo2['spo2'] = da['spo2']
        temp_spo2['hr'] = da['heartrate']
        temp_spo2['wear_type'] = da['wear_type']
        temp_spo2['timestamp'] = da['timestamp'].map(Str_Change_Time(2))
        temp_spo2['cost'] = da['wear_data'].map(Str_Chnage_data(5))
        temp_spo2['cost_all'] = da['wear_data'].map(Str_Chnage_data(6))
        temp_spo2['cost_cnt'] = da['wear_data'].map(Str_Chnage_data(9))
        temp_spo2['healthindex'] = da['healthindex'].map(Bad_output)
    else:
        temp_spo2 = []

    return temp_spo2



def Choose_time(checklist):
    start = 9
    end = 23

    if len(str(checklist)) < 6 :
        mm = int(str(checklist)[2])
    else:
        mm = int(str(checklist)[2:4])

    if mm == 0:
        start = 9
        end = 23
    else:
        if int(mm % 3) == 0:
            start = 9
        else:
            start = 6 + int(mm % 3)

        if mm > 9:
            end = 21 + int((mm + 2) / 4)
        elif mm > 6:
            end = 21 + int((mm + 1) / 4)
        else:
            end = 21 + int((mm) / 4)
    return start,end



def Com_Rate(data_wear,checklist):
    data_wear['Hour'] = 0
    data_wear['Hour'] = data_wear['datetime'].map(Time_get(1))

    rate_all = Get_rate(data_wear)
    start, end = Choose_time(checklist)

    data_night1 = data_wear[data_wear['Hour'] <= start]
    data_night2 = data_wear[data_wear['Hour'] >= end]
    data_night = pd.merge(data_night1, data_night2, how='outer')
    rate_night1 = Get_rate(data_night)

    data_day = data_wear[data_wear['Hour'] > start]
    data_day = data_day[data_day['Hour'] < end]
    rate_day1 = Get_rate(data_day)

    return rate_all,rate_night1,rate_day1



def Get_rate(data):
    if len(data) > 5:
        data_usable_hr = data[data['spo2'] > 0]
        data_usable = data_usable_hr[data_usable_hr['heartrate'] > 0]
        try:
            rate = len(data_usable) / len(data) * 100
        except ZeroDivisionError:
            rate = 0
    else:
        rate = 0

    rate = float('%.2f' % rate)
    return rate
rate_save = pd.DataFrame(np.arange(10), columns=['timesta'])




