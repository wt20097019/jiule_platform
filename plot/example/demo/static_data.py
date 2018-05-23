# coding=utf8
"""
Created on Thu May 10 16:10:33 2018

@author: twang

用于统计分析页面数据的展示
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from io import StringIO
import time
from collections import Counter

from .Changef import  Str_Change_Time,Str_Chnage_data,num


str_path1 = 'http://api.jiuletech.com/data/t3_data.php?filter_name='
str_path2 = 'http://api.jiuletech.com/test/t3_data.php?filter_name='
str_path3 = 'http://api.releasetest.jiuletech.com/data/t3_data.php?filter_name='


def change_str(cnt):
    strout = str(cnt)
    length = len(strout)
    strout = strout[0:length-2]
    return strout


def plotshow(pro):

    data = pro[pro['time_cost'] > 0]
    data = data[data['spo2'] > 0]
    data = data[data['heartrate'] > 0]

    data1 = data['time_cost']
    mean = data1.mean()
    mean = float('%.1f' % mean)

    f, ax = plt.subplots(dpi=400, figsize=(10, 4))

    ax = sns.distplot(data1, bins=60, rug=False,color='r')

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    ax.tick_params(axis='x', labelsize=12)  # y轴
    ax.tick_params(axis='y', labelsize=12)  # y轴
    strplot = '平均时长:' + str(mean) + 's'
    ax.set_title(strplot, fontsize=12)
    ax.set_xlabel('Time/s', fontsize=14)

    f.savefig("example\static\show.jpg", dpi=400, bbox_inches='tight')


def plotshow1(pro):

    pro['time'] = 16* pro['timestamp'].map(Str_Change_Time(0))
    show = pro[pro['time_cost'] > 0]
    show = show[show['spo2'] > 0]
    show = show[show['heartrate'] > 0]
    grouped = show['time_cost'].groupby(show['time'])
    t = grouped.mean()

    f, ax = plt.subplots(dpi=100, figsize=(10, 4))
    xmajorLocator = plt.MultipleLocator(16)
    sns.barplot(x=t.index, y=t)

    ax.tick_params(axis='x', labelsize=0)  # y轴
    ax.tick_params(axis='y', labelsize=8)  # y轴
    ax.xaxis.set_major_locator(xmajorLocator)
    ax.set_xlabel('Time/H', fontsize=12)
    ax.set_ylabel('time_cost/s', fontsize=10)
    f.savefig("example\static\show1.jpg", dpi=400, bbox_inches='tight')


def plotshow2(pro):

    pro['time'] = 16* pro['timestamp'].map(Str_Change_Time(0))
    pro = pro[pro['time_cost_all'] > 0]
    pro = pro[pro['healthindex'] != 220]
    grouped = pro['time_cost_all'].groupby(pro['time'])
    t = grouped.mean()

    f, ax = plt.subplots(dpi=100, figsize=(10, 4))
    xmajorLocator = plt.MultipleLocator(16)
    sns.barplot(x=t.index, y=t)

    ax.tick_params(axis='x', labelsize=0)  # y轴
    ax.tick_params(axis='y', labelsize=8)  # y轴
    ax.xaxis.set_major_locator(xmajorLocator)
    ax.set_xlabel('Time/H', fontsize=12)
    ax.set_ylabel('All_cost/s', fontsize=10)
    f.savefig("example\static\show2.jpg", dpi=400, bbox_inches='tight')


def plotshow3(pro):
    grouped = pro['time_cost_all'].groupby(pro['time_send'])
    hh = grouped.mean()

    m = pd.Series.to_frame(hh)
    m['time'] = m.index
    m[' '] = 'After'

    t = pd.read_csv('before.csv')

    mean1 = t['time_cost_all'].mean()
    mean2 = m['time_cost_all'].mean()

    temp1 = pd.DataFrame(np.arange(2), columns=['time_cost_all'])
    temp1['time'] = 0
    temp1[' '] = 0

    temp1.iloc[0, 0] = 0
    temp1.iloc[0, 1] = ' '
    temp1.iloc[0, 2] = 'Before'

    temp1.iloc[1, 0] = mean1
    temp1.iloc[1, 1] = 'All'
    temp1.iloc[1, 2] = 'Before'
    t = pd.merge(t, temp1, how='outer')

    temp1['time'] = 0
    temp1[' '] = 0

    temp1.iloc[0, 0] = 0
    temp1.iloc[0, 1] = ' '
    temp1.iloc[0, 2] = 'After'

    temp1.iloc[1, 0] = mean2
    temp1.iloc[1, 1] = 'All'
    temp1.iloc[1, 2] = 'After'
    m = pd.merge(m, temp1, how='outer')

    out = pd.merge(t, m, how='outer')
    out['time'] = out['time'].map(change_str)

    f, ax = plt.subplots(dpi=400, figsize=(10, 4))
    ax = sns.barplot(x="time", y="time_cost_all", hue=" ", data=out, palette=sns.color_palette("Set2", 2), capsize=.1)
    ax.tick_params(axis='x', labelsize=10)  # y轴
    ax.tick_params(axis='y', labelsize=8)  # y轴
    ax.set_xlabel('Time/H', fontsize=12)
    ax.set_ylabel('time_cost/s', fontsize=10)

    f.savefig("example\static\show3.jpg", dpi=400, bbox_inches='tight')


"""成功率-次数对比图"""
def  plotshow4(pro):

    data = pro[pro['time_cost'] > 0]
    data = data[data['spo2'] > 0]
    data = data[data['heartrate'] > 0]

    hg = pro[pro['time_cnt'] <= 7]['time_cnt']
    hg2 = data['time_cnt']

    res = Counter(hg)
    res1 = Counter(hg2)

    rate = pd.DataFrame(np.arange(7), columns=['rate'])
    rate2 = pd.DataFrame(np.arange(7), columns=['rate'])
    for i in range(7):
        rate.iloc[i, 0] = res1[i + 1] / res[i + 1]
        rate2.iloc[i, 0] = res[i + 1]

    rate.index = np.arange(1, 8)
    labels = ['1', '2', '3', '4', '5', '6', '7']

    sns.set(style='darkgrid', palette='deep', color_codes=True)
    f, ax = plt.subplots(dpi=200, figsize=(5, 4))
    ax = sns.barplot(x=rate.index, y=rate['rate'], data=rate)
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    strg = '成功率-次数对比图'
    ax.set_title(strg, fontsize=12)
    ax.set_xlabel('Time_cnt', fontsize=12)
    ax.set_ylabel('SuccessRate', fontsize=10)
    f.savefig("example\static\show4.jpg", dpi=200, bbox_inches='tight')

    f, ax = plt.subplots(dpi=200, figsize=(4, 4))
    ax = plt.pie(rate2, labels=labels)
    f.savefig("example\static\show5.jpg", dpi=200, bbox_inches='tight')





""" 将结果绘制为图片,进行展示 """
def savefig():
    sns.set(color_codes=True)

    today = time.strftime('%Y-%m-%d', time.localtime(time.time()))

    path = 'http://api.releasetest.jiuletech.com/data/t3_upgrade.php'
    data2 = pd.read_html(path)[0]
    data = data2.drop([0])
    data[2] = data[2].map(num)

    data = data[data[2] >= 30113]
    listname = data[1]
    listname.index = np.arange(len(listname))

    pydata = {'export_wear': '导出16428数据',
              'filter_start_date': '2018-03-01',
              'filter_to_date': '2018-03-09'}

    str_path = 'http://api.releasetest.jiuletech.com/data/t3_data.php?filter_name='

    """多人数据的拼接"""
    for i in range(len(listname)):
        mm = listname[i]
        username = mm
        date = '2018-04-30'
        str_CCID = '导出' + username + '数据'
        pydata['export_wear'] = str_CCID
        pydata['filter_start_date'] = date
        pydata['filter_to_date'] = today

        path1 = str_path + username

        try:
            r = requests.post(path1, data=pydata)
        except requests.ConnectionError:
            a = 1
        else:
            imgBuf = StringIO(r.text)
            df = pd.read_csv(imgBuf)
        if i > 0:
            pro = pd.merge(pro, df, how='outer')
        else:
            pro = df

    """数据转换"""
    pro['time_cost'] = pro['wear_data'].map(Str_Chnage_data(5))
    pro['time_cost_all'] = pro['wear_data'].map(Str_Chnage_data(6))
    pro['time_send'] = pro['timestamp'].map(Str_Change_Time(3))
    pro['time_cnt'] = pro['wear_data'].map(Str_Chnage_data(7))

    plotshow4(pro)
    plotshow(pro)
    plotshow1(pro)
    plotshow2(pro)
    plotshow3(pro)











