# coding=utf8


from django.db.models import Count
from pyecharts import Line, Pie, Page, Bar

from django_echarts.views.backend import EChartsBackendView
from django_echarts.datasets.fetch import fetch
from demo import models
from .demo_data import create_simple_bar, create_simple_kline, create_simple_pie,Data_for_static
from django.shortcuts import render
from django.http import HttpResponse
from django import forms
import pandas as pd
import numpy as np
import re
import requests
from io import StringIO
from bs4 import BeautifulSoup as bs
import threading
import time





str_path = 'http://api.jiuletech.com/test/t3_data.php?filter_name='

a = '16141'
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


def Str_Chage5(strchange):
    data_value = int(strchange[22:24], 16) * 256 + int(strchange[24:26], 16)
    return data_value


def Str_Chage6(strchange):
    data_value = int(strchange[21], 16) & 1
    return data_value


def Str_Change_time(strchange):
    time_local = time.localtime(strchange)
    time_pro = time.localtime(strchange)
    if time_pro[3] + time_pro[4] / 60 > 0:
        data_value = time_pro[3] + time_pro[4] / 60 - 0.0833
        data_value = float('%.2f' % data_value)
    else:
        data_value = time_pro[3] + time_pro[4] / 60
        data_value = float('%.2f' % data_value)
    return data_value


def Str_Change_time2(strchange):
    time_local = time.localtime(strchange)
    time_pro = time.localtime(strchange)
    if time_pro[3] + time_pro[4] / 60 > 0:
        data_value = time_pro[3] + time_pro[4] / 60
        data_value = float('%.2f' % data_value)
    else:
        data_value = time_pro[3] + time_pro[4] / 60 + 0.01
        data_value = float('%.2f' % data_value)
    return data_value


def Change_Str_Data(da):
    length = len(da)
    temp1 = pd.DataFrame(np.arange(length), columns=['timestamp'])
    temp1['wear_data'] = da['wear_data'].map(Str_Chage_N(14))
    temp2 = pd.DataFrame(np.arange(length), columns=['timestamp'])
    temp2['wear_data'] = da['wear_data'].map(Str_Chage_N(12))

    temp1['timestamp'] = da['timestamp'].map(Str_Change_time)
    temp2['timestamp'] = da['timestamp'].map(Str_Change_time2)

    temp1['Activity'] = da['wear_data'].map(Str_Chage_N(18))
    temp2['Activity'] = da['wear_data'].map(Str_Chage_N(16))

    temp1['movement'] = da['wear_data'].map(Str_Chage5)
    temp2['movement'] = da['wear_data'].map(Str_Chage5)

    temp1['Charge'] = da['wear_data'].map(Str_Chage6)
    temp2['Charge'] = da['wear_data'].map(Str_Chage6)

    temp1['Wear_type'] = da['wear_type']
    temp2['Wear_type'] = da['wear_type']

    temp1['activity'] = da['activity']
    temp2['activity'] = da['activity']

    temp3 = pd.merge(temp1, temp2, how='outer')
    temp3 = temp3.sort_values(axis=0, ascending=True, by='timestamp')
    temp3.index = np.arange(len(temp3))
    return temp3


def Change(str1):
    aa = float(re.findall(r"\d+\.?\d*",str1)[0])
    return aa



def create_simple_mm():
    global a

    a = str(a)
    UserName = a
    pydata = {'export_wear': '导出16428数据',
              'filter_start_date': '2018-03-15',
              'filter_to_date': '2018-03-15'}
    str_CCID = '导出' + a + '数据'

    TimeString = str(2018) + '-' + str(3) + '-' + str(15) + ' ' + '0:00:00'
    TimeStampChoose = int(time.mktime(time.strptime(TimeString, '%Y-%m-%d %H:%M:%S')))

    x = time.localtime(TimeStampChoose)  # localtime参数为float类型，这里y1317091800.0为float类型
    x2 = time.localtime(TimeStampChoose - 86400)
    str_date1 = time.strftime('%Y-%m-%d', x)
    str_date2 = time.strftime('%Y-%m-%d', x2)

    str_CCID = '导出'+a+'数据'
    pydata['export_wear'] = str_CCID
    pydata['filter_start_date'] = str_date2
    pydata['filter_to_date'] = str_date1

    path = str_path + UserName
    r = requests.post(path, data=pydata)
    imgBuf = StringIO(r.text)
    df = pd.read_csv(imgBuf)

    da = df.sort_values(axis=0, ascending=True, by='timestamp')

    da = da[da['timestamp'] >= TimeStampChoose]
    length1 = len(da)
    da.index = np.arange(length1)
    temp3 = Change_Str_Data(da)

    data_x = temp3['timestamp']
    train_data = np.array(data_x)
    train_x_list = train_data.tolist()  # list

    data_x = temp3['wear_data']
    train_data = np.array(data_x)
    train_y_list = train_data.tolist()  # list

    attr = ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
    v1 = [5, 20, 36, 10, 10, 100]
    v2 = [55, 60, 16, 20, 15, 80]
    line = Line("电容值波动情况")

    str2 = a + "Wear_Data"
    line.add(str2, train_x_list, train_y_list)
    line.render()
    return line




ECHARTS_DICT = {
    'bar': create_simple_bar,
    'kine': create_simple_kline,
    'pie': create_simple_pie,
    'add': create_simple_mm,
}


class AddForm(forms.Form):
    a = forms.IntegerField()
    b = forms.IntegerField()



class BackendEChartsTemplate(EChartsBackendView):
    template_name = 'backend_charts.html'

    def get_echarts_instance(self, *args, **kwargs):
        name = self.request.GET.get('name', 'bar')
        if name not in ECHARTS_DICT:
            name = 'bar'
        return ECHARTS_DICT[name]()


class TemperatureEChartsView(EChartsBackendView):
    echarts_instance_name = 'line'
    template_name = 'temperature_charts.html'

    def get_echarts_instance(self, **kwargs):
        context = super(TemperatureEChartsView, self).get_context_data(**kwargs)
        t_data = models.TemperatureRecord.objects.all().order_by('create_time').values_list('high', 'create_time')
        hs, ds = zip(*t_data)
        line = Line('High Temperature')
        line.add('High', ds, hs)
        context['line'] = line
        return context


class PageDemoView(EChartsBackendView):
    echarts_instance_name = 'page'
    template_name = 'page_demo.html'

    def get_echarts_instance(self, **kwargs):
        return Data_for_static()





