# coding=utf8


from django.views.generic.base import TemplateView
from django_echarts.views.frontend import EChartsFrontView
from .demo_data import create_simple_bar, create_simple_kline, create_simple_pie,save_username,save_date,Data_Acquire,Data_for_static,save_list,Name_list,Version_Get,Name_title,Get_ccid
from .static_data import savefig
from . import forms
from django.shortcuts import render
import datetime
import time
from django.http import HttpResponse
import requests

username = '16480'
date = '2018-03-15'

ui = 0
class IndexView(TemplateView):
    template_name = 'index.html'


class Frontend_charts(TemplateView):
    create_simple_bar()
    template_name = 'frontend_charts.html'


class SimpleBarView(EChartsFrontView):
    global ui
    def get_echarts_instance(self, **kwargs):
        global ui
        ui = 0
        return create_simple_bar()


class SimpleKLineView(EChartsFrontView):
    global ui
    def get_echarts_instance(self, **kwargs):
        global ui
        ui = 1
        return create_simple_kline()


class SimpleMapView(EChartsFrontView):
    global ui
    def get_echarts_instance(self, **kwargs):
        global ui
        ui = 3
        return create_simple_map()


class SimplePieView(EChartsFrontView):
    global ui
    def get_echarts_instance(self, **kwargs):
        global ui
        ui = 2
        return create_simple_pie()

class SimpleDataView(EChartsFrontView):
    global date
    global ui
    def get_echarts_instance(self, **kwargs):
        global ui
        global date
        date = date + datetime.timedelta(days=1)
        save_date(date)
        Data_Acquire()
        if ui == 0:
            return create_simple_bar()
        elif ui == 1:
            return create_simple_kline()
        elif ui == 2:
            return create_simple_pie()
        else :
            return create_simple_bar()

class SimpleData1View(EChartsFrontView):
    global date
    def get_echarts_instance(self, **kwargs):
        global date
        date = date + datetime.timedelta(days=-1)
        save_date(date)
        Data_Acquire()
        if ui == 0:
            return create_simple_bar()
        elif ui == 1:
            return create_simple_kline()
        elif ui == 2:
            return create_simple_pie()
        else:
            return create_simple_bar()

line = 0
flag = 0
namelist = []
class SimpleListDnView(EChartsFrontView):
    global date
    global namelist
    global line
    global  flag
    global m_version
    def get_echarts_instance(self, **kwargs):
        global line
        global flag
        global namelist
        namelist = Name_list()

        if len(namelist) <= 10:
            Data_Acquire()
            namelist = Name_list()

        if line < (len(namelist) - 1):
            line = line + 1

        username = namelist[line]
        save_username(username)

        Data_Acquire()
        if ui == 0:
            return create_simple_bar()
        elif ui == 1:
            return create_simple_kline()
        elif ui == 2:
            return create_simple_pie()
        else:
            return create_simple_bar()


class SimpleListUpView(EChartsFrontView):
    global date
    global namelist
    global line
    global  flag
    global title
    global m_version
    global username


    def get_echarts_instance(self, **kwargs):
        global line
        global flag
        global namelist
        global date

        namelist = Name_list()
        if len(namelist) <= 10:
            Data_Acquire()
            namelist = Name_list()

        if line > 1:
            line = line - 1

        username = namelist[line]
        save_username(username)
        Data_Acquire()

        if ui == 0:
            return create_simple_bar()
        elif ui == 1:
            return create_simple_kline()
        elif ui == 2:
            return create_simple_pie()
        else:
            return create_simple_bar()

class SimpleRateView(EChartsFrontView):
    global date
    def get_echarts_instance(self, **kwargs):
        return Data_for_static()



def login(request):
    global username
    global dataframe
    global date
    global title
    global m_version
    global namelist

    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            date = login_form.cleaned_data['datetime']


        save_username(username)
        save_date(date)
    title = Name_title()
    m_version = Version_Get()
    #m_version = '30119'
    t_date = request.GET.get('t_date')
    t_name = request.GET.get('t_name')
    t_version = request.GET.get('t_version')
    if t_date != None  or t_name != None :
        title = Name_title()
        username = Get_ccid()
        title1 = username[-5:] + '-' + title
        send = str(date) + '/' + title1 +'/' +  m_version
        return HttpResponse(send)

    return render(request, 'login.html', {'date': date, 'username': username, 'title': title, 'm_version': m_version})


def choose(request):
    global user_version
    global namelist
    check_box_list = request.POST.getlist("select_list")
    save_list(check_box_list)
    save_date(date)
    title = Name_title()
    m_version = Version_Get()
    return render(request, 'login.html', {'date': date, 'username': username, 'title': title, 'm_version': m_version})



image_flag = 0
def show(request):
    global image_flag
    if image_flag == 0:
        savefig()
        image_flag = 1
    return render(request, 'show.html', locals())




