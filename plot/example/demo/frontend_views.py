# coding=utf8


from django.views.generic.base import TemplateView
from django_echarts.views.frontend import EChartsFrontView
from .demo_data import create_simple_bar, create_simple_kline, create_simple_pie,save_username,save_date,Data_Acquire,Data_for_static,save_list,Name_list
from .static_data import savefig
from . import forms
from django.shortcuts import render
import datetime
import requests


ui = 0
class IndexView(TemplateView):
    template_name = 'index.html'


class FrontendEchartsTemplate(TemplateView):
    template_name = 'login.html'


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
    def get_echarts_instance(self, **kwargs):
        global line
        global flag
        global namelist

        namelist = Name_list()
        if len(namelist) <= 10:
            Data_Acquire()
        if flag == 0:
            namelist = Name_list()
            flag = 1

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

    def get_echarts_instance(self, **kwargs):
        global line
        global flag
        global namelist

        namelist = Name_list()
        if len(namelist) <= 10:
            Data_Acquire()

        if flag == 0:
            namelist = Name_list()
            flag = 1

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

username = '16480'
date = '2018-03-15'
def login(request):
    global username
    global dataframe
    global date
    if request.method == "POST":
            login_form = forms.UserForm(request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data['username']
                date = login_form.cleaned_data['datetime']
    login_form = forms.UserForm()
    save_username(username)
    save_date(date)
    return render(request, 'login.html', {'form': login_form})


def choose(request):
    check_box_list = request.POST.getlist("check_box_list")
    save_list(check_box_list)
    return render(request, 'login.html', locals())

image_flag = 0
def show(request):
    global image_flag
    if image_flag == 0:
        savefig()
        image_flag = 1
    return render(request, 'show.html', locals())





