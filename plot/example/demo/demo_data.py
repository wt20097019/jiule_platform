# coding=utf8

from pyecharts import Bar, Kline, Map, Pie,Line,Grid,Scatter,Overlap,Page
import pandas as pd
import numpy as np
import re
import datetime
import calendar
from datetime import datetime,timedelta

from scipy import stats, integrate
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from io import StringIO
import time
import threading

from .Changef import  Str_Change_Time,Str_Chnage_data,Change_Str_Data,num,abs_diff,Bad_output,Time_get,Str_Chage_N,Data_martix,Choose_time,Com_Rate,Get_rate



#str_path = 'http://api.releasetest.jiuletech.com/data/t3_data.php?filter_name='
str_path = 'http://api.jiuletech.com/data/t3_data.php?filter_name='
str_path1 = 'http://api.jiuletech.com/data/t3_data.php?filter_name='
#str_path1 = 'http://api.releasetest.jiuletech.com/data/t3_data.php?filter_name='
str_path2 = 'http://api.jiuletech.com/test/t3_data.php?filter_name='
str_path3 = 'http://api.releasetest.jiuletech.com/data/t3_data.php?filter_name='

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
           'Cache-Control': 'max-age=0',
           'Host': 'api.jiuletech.com',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:59.0) Gecko/20100101 Firefox/59.0',
           'Connection': 'keep-alive',
           'Upgrade-Insecure-Requests': '1',
           'Authorization': 'Basic aml1bGV0ZWNoOkppdUxl',
           'Referer': 'http://api.jiuletech.com/data/t3_data.php?filter_start_date=2018-04-15&filter_to_date=2018-05-15&filter_name=16428&s=0'
           }

name = 0
flag = 0
rate = 50
title = ' '
list_flag = 0

username = '16480'
date_pro = '2018-03-15'

"""其他文件的全局变量调用方法"""
def save_username(a):
    global username
    username = a

"""其他文件的全局变量调用方法"""
def save_date(a):
    global date_pro
    date_pro = a

checklist = ['0']
def save_list(a):
    global checklist
    checklist = a



def Get_ccid():
    global username
    return username
listname = []
mersion = '30119'

def Name_list():
    global list_flag
    global listname
    global Version
    global headers
    global leng

    if list_flag == 0:

        if str_path == str_path1:

            Version_Get()
            pydata = {
                'filter_name': 'V30122',
                'page':'1'}

            url = 'http://api.jiuletech.com/data/t3_upgrade.php?filter_name=' + Version

            headers['Referer'] = 'http://api.jiuletech.com/data/t3_upgrade.php?filter_name=16480'
            m1 = pd.DataFrame(np.arange(0), columns=['timestamp'])
            for j in range(5):
                pydata['filter_name'] = Version
                pydata['page'] = str(j + 1)

                url = 'http://api.jiuletech.com/data/t3_upgrade.php?filter_name=' + Version + '&page=' + str(j + 1)
                length_list = 0
                try:
                    r = requests.post(url, headers=headers, data=pydata)
                except:
                    page_source = []
                    length_list = 0
                else:
                    page_source = r.text
                    aa = re.findall(r'<td[^>]*>(.*?)</td>', page_source)
                    length_list = int(len(aa) / 8)

                if length_list > 1:
                    m = pd.DataFrame(np.arange(length_list), columns=['timestamp'])
                    for i in range(length_list):
                        m.iloc[i, 0] = aa[8 * i + 1]
                    m1 = pd.merge(m1, m, how='outer')

                if length_list < 29:
                    break

            if len(m1) >= 2:
                listname = m1['timestamp']
                listname.index = np.arange(len(listname))

        else:
            if str_path == str_path2:
                path = 'http://api.jiuletech.com/test/t3_upgrade.php?filter_name='
            elif str_path == str_path3:
                path = 'http://api.releasetest.jiuletech.com/data/t3_upgrade.php?filter_name='
            Version_Get()
            path = path + Version
            data2 = pd.read_html(path)[0]
            data = data2.drop([0])
            listname = data[1]
            listname.index = np.arange(len(listname))
            list_flag = 1
    leng = len(listname)
    return listname



"""将dataFrame转换为用于显示的list结构"""
def data_to_list(str_choose):
    if str_choose == "Charge":
        data_x = temp3[str_choose] + 0.1
    else:
        data_x = temp3[str_choose]
    train_data = np.array(data_x)
    train_list = train_data.tolist()  # list
    return train_list


"""对dataFrame进行填充转换为用于显示的list结构"""
def data_fill(str_choose):
    global temp3
    global com

    temp1 = pd.DataFrame(np.arange(288), columns=['timestamp'])
    temp1['timestamp'] = com['timestamps']
    temp1['data'] = 0

    if len(temp3) > 1:
        temp2 = pd.DataFrame(np.arange(len(temp3['timestamps'])), columns=['timestamp'])
        temp2['timestamp'] = temp3['timestamps']
        temp2['data'] = temp3[str_choose]
    else:
        temp2 = pd.DataFrame(np.arange(1), columns=['timestamp'])
        temp2['timestamp'] = 0
        temp2['data'] = 0

    temp = pd.merge(temp1, temp2, how='left', on=['timestamp'])
    temp5 = pd.DataFrame(np.arange(288), columns=['data'])
    temp4 = temp['data_y']

    if str_choose == 'channel1' or str_choose == 'channel2' or str_choose == 'channel3':
        temp5['data'] = temp4.fillna(700)
    else:
        if str_choose == 'Wear_type' or str_choose == 'Charge':
            temp5['data'] = temp4.fillna(-10)
        else:
            temp5['data'] = temp4.fillna(0)

    temp5['timestamp'] = temp1['timestamp']

    if str_choose == 'timestamp':
        data_m = temp5['timestamp']
        train_data_m = np.array(data_m)
        train_list = train_data_m.tolist()  # list
    else:
        if str_choose == 'Charge':
            data_m = temp5['data'] + 0.1
        else:
            data_m = temp5['data']
        train_data_m = np.array(data_m)
        train_list = train_data_m.tolist()  # list
    return train_list



def Normalize(N):
    global max_channel1
    global max_channel2
    global max_channel3
    def  channel_pro(channel):
        global max_channel1
        global max_channel2
        global max_channel3

        if N == 1:
            max_Data = max_channel1
        elif N == 2:
            max_Data = max_channel2
        elif N == 3:
            max_Data = max_channel3
        if max_Data >0:
            Nor_channel =channel / max_Data *1000
        else:
            Nor_channel = 0
        return Nor_channel
    return channel_pro



def data_to_list_spo2(temp_s,str_choose):
    data_x = temp_s[str_choose]
    train_data = np.array(data_x)
    train_list = train_data.tolist()  # list
    return train_list


def  fill_data(temp_sp2,strinput):
    temp1 = pd.DataFrame(np.arange(144), columns=['cnt'])

    if len(temp_sp2) > 0:
        temp2 = pd.DataFrame(np.arange(len(temp_sp2)), columns=['cnt'])
        temp2['cnt'] = temp_sp2['timestamp']
        temp2['data'] = temp_sp2[strinput]
    else:
        temp2 = pd.DataFrame(np.arange(1), columns=['cnt'])
        temp2['cnt'] = 0
        temp2['data'] = 0

    for i in range(145):
        j = i % 6
        n = int(i / 6)
        if j == 0:
            m = 0
        elif j == 1:
            m = 0.2
        elif j == 2:
            m = 0.3
        elif j == 3:
            m = 0.5
        elif j == 4:
            m = 0.7
        elif j == 5:
            m = 0.8
        temp1.loc[i, 'cnt'] = n + m

    temp1['data'] = 0

    temp3 = pd.merge(temp1, temp2, how='left', on=['cnt'])
    temp4 = temp3['data_y']
    temp5 = pd.DataFrame(np.arange(145), columns=['cnt'])
    temp5['data'] = temp4.fillna(0)
    temp5['cnt'] = temp1['cnt']

    data_m = temp5['cnt']
    train_data_m = np.array(data_m)
    train_t_list = train_data_m.tolist()  # list

    data_m = temp5['data']
    train_data_m = np.array(data_m)
    train_w_list = train_data_m.tolist()  # list

    return train_t_list,train_w_list




date_upgrade = '2018-05-17'
"""获取用户名"""
old_username = ''
def  Name_title():
    global username
    global str_path
    global old_username
    global date_pro
    global title
    global date_upgrade

    pydata = {'filter_name': '16480',
              'filter_start_date': '2018-03-01',
              'filter_to_date': '2018-03-09'}

    url = 'http://api.jiuletech.com/data/t3_data.php?filter_name=' + username


    if old_username == username:
        old_username = username
    else:
        TimeString = str(date_pro) + ' ' + '0:00:00'
        TimeStampChoose = int(time.mktime(time.strptime(TimeString, '%Y-%m-%d %H:%M:%S')))

        x = time.localtime(TimeStampChoose)  # localtime参数为float类型，这里y1317091800.0为float类型
        x1 = time.localtime(TimeStampChoose - 86400*5 )  # localtime参数为float类型，这里y1317091800.0为float类型
        today = time.strftime('%Y-%m-%d', x)
        date = time.strftime('%Y-%m-%d', x1)
        path = str_path  + username + '&filter_start_date=' + date + '&filter_to_date=' + today

        if str_path == str_path1:
            date = datetime.strptime(date_upgrade, '%Y-%m-%d')
            date = date + timedelta(days=-1)
            detester = date.strftime('%Y-%m-%d')
            pydata['filter_start_date'] = detester

            pydata['filter_to_date'] = date_upgrade
            pydata ['filter_name'] = username

            try:
                r = requests.post(url, headers=headers, data=pydata)
            except requests.ConnectionError:
                aa = []
            else:
                page_source = r.text
                aa = re.findall(r'<td[^>]*>(.*?)</td>', page_source)

            if len(aa) >= 18:
                title = aa[2]
            else:
                title = 'Test1 '

        else:
            data = pd.read_html(path)[0]
            if len(data) >= 2:
                title = str(data.iloc[2,2])
                old_username = username
            else:
                title = ''

    return title


Version = '30119'
"""获取版本号"""
def  Version_Get():
    global str_path
    global username
    global Version
    global headers
    global date_upgrade

    if str_path == str_path1:
        pydata = {
            'filter_name': '16480'}

        url = 'http://api.jiuletech.com/data/t3_upgrade.php?filter_name=' + username
        pydata['filter_name'] = username
        headers['Referer'] = 'http://api.jiuletech.com/data/t3_upgrade.php?filter_name='
        try:
            r = requests.post(url, headers=headers, data=pydata)
        except requests.ConnectionError:
            aa = []
        else:
            page_source = r.text
            aa = re.findall(r'<td[^>]*>(.*?)</td>', page_source)

        if len(aa) >= 1:
            Version = aa[2]
            date_upgrade = aa[7][0:10]
        else:
            Version = ''
    else:
        if str_path == str_path2:
            str_path_version = 'http://api.jiuletech.com/test/t3_upgrade.php?filter_name='

        elif str_path == str_path3:
            str_path_version = 'http://api.releasetest.jiuletech.com/data/t3_upgrade.php?filter_name='

        path = str_path_version + username
        data2 = pd.read_html(path)[0]
        data2 = data2.drop([0])
        m_version = str(data2[2])
        Version = m_version[6:11]

    return Version



def getMonthFirstDayAndLastDay(year=None, month=None):
    if year:
        year = int(year)
    else:
        year = datetime.date.today().year

    if month:
        month = int(month)
    else:
        month = datetime.date.today().month

    # 获取当月第一天的星期和当月的总天数
    firstDayWeekDay, monthRange = calendar.monthrange(year, month)

    return  monthRange



"""电容波动情况的图形页面绘制"""
def create_simple_bar():
    global temp3
    global str_path
    global name
    global flag
    global com
    global date_pro
    global username
    global title

    global max_channel1
    global max_channel2
    global max_channel3

    global h
    global leng

    Data_Acquire()
    temp3 = Change_Str_Data(da)

    if flag == 0:
        com = temp3
        flag = 1

    """三个通道的电容值进行归一化处理"""

    if len(temp3) > 0:
        max_channel1 = temp3['channel1'].max()
        max_channel2 = temp3['channel2'].max()
        max_channel3 = temp3['channel3'].max()
        """
        temp3['channel1'] = temp3['channel1']/max_channel1*1000
        temp3['channel2'] = temp3['channel2'] / max_channel2 * 1000
        temp3['channel3'] = temp3['channel3'] / max_channel3 * 1000
        """

        temp3['channel1'] = temp3['channel1'].map(Normalize(1))
        temp3['channel2'] = temp3['channel2'].map(Normalize(2))
        temp3['channel3'] = temp3['channel3'].map(Normalize(3))


    """数据未达到指定组数时进行数据填充"""
    if len(temp3) < 280:
        train_x_list = data_fill('timestamp')  # list
        train_y_list = data_fill('wear_data')
        train_z_list = data_fill('Wear_type')
        train_k_list = data_fill('channel1')
        train_l_list = data_fill('channel2')
        train_a_list = data_fill('channel3')
        train_o_list = data_fill('Charge')
        train_b_list = data_fill('Activity')
        train_c_list = data_fill('activity')
    else:
        """将dataFrame格式转为list"""
        train_x_list = data_to_list('timestamp')  # list
        train_y_list = data_to_list('wear_data')
        train_z_list = data_to_list('Wear_type')
        train_k_list = data_to_list('channel1')
        train_l_list = data_to_list('channel2')
        train_a_list = data_to_list('channel3')
        train_b_list = data_to_list('Activity')
        train_c_list = data_to_list('activity')
        train_o_list = data_to_list('Charge')

    plotstr2 = str(leng) + str(date_pro) + '/' + username + '-' + title + ': ' + "检测结论----该段时间内数据正常"
    line2 = Line("Mems波动值", plotstr2)
    strm = "Mems波动值"
    strn = "活动量"
    line2.add(strm, train_x_list, train_b_list, yaxis_min="dataMin", legend_top="1%")
    line2.add(strn, train_x_list, train_c_list, yaxis_min="dataMin", legend_top="1%")

    line3 = Line("三通道归一化后变化", title_top="50%")
    strc1 = "Chnanel1"
    strc2 = "Chnanel2"
    strc3 = "Chnanel3"
    line3.add(strc1, train_x_list, train_k_list, yaxis_min=700, legend_top="51%")
    line3.add(strc2, train_x_list, train_l_list, yaxis_min=700, legend_top="51%")
    line3.add(strc3, train_x_list, train_a_list, yaxis_min=700, legend_top="51%")

    line1 = Scatter("佩戴/充电状态", title_top="75%")
    strm = "佩戴状态"
    line1.add(strm, train_x_list, train_z_list, xaxis_max=24, yaxis_min=0, yaxis_max=1.2, legend_top="76%")
    line1.add('充电状态', train_x_list, train_o_list, xaxis_max=24, yaxis_min=0, yaxis_max=1.2, legend_top="76%",
              symbol_size=5, xaxis_name='Time/H')

    line = Line("电容波动情况", title_top="25%")
    strm = "电容值波动情况"
    line.add(strm, train_x_list, train_y_list, yaxis_min=0, legend_top="26%", label_color="#40ff27")

    page = Grid()
    page.add(line3, grid_top="55%", grid_bottom="30%")
    page.add(line1, grid_top="80%", grid_bottom="5%")
    page.add(line, grid_top="30%", grid_bottom="55%")
    page.add(line2, grid_top="5%", grid_bottom="80%")
    page.renderer = 'svg'
    return page



"""血氧心率页面图形绘制"""
def create_simple_kline():
    global username
    global temp_spo2
    global temp3
    global date_pro
    global rate_all
    global rate_night1
    global rate_day1
    global checklist
    global title
    global da

    temp_spo2 = Data_martix(da)

    if len(temp_spo2) > 1:
        train_x_list = data_to_list_spo2(temp_spo2,'timestamp')
        train_y_list = data_to_list_spo2(temp_spo2,'spo2')
        train_z_list = data_to_list_spo2(temp_spo2,'hr')

        temp_spo3 = temp_spo2[temp_spo2['healthindex'] > 0]
        data_x = temp_spo3['healthindex']
        train_data = np.array(data_x)
        train_e_list = train_data.tolist()  # list

        data_x = temp_spo3['timestamp']
        train_data = np.array(data_x)
        train_r_list = train_data.tolist()  # list

        dd = temp_spo2[temp_spo2['healthindex'] ==15]

        train_t_list = data_to_list_spo2(temp_spo2, 'timestamp')
        train_k_list = data_to_list_spo2(temp_spo2, 'wear_type')
        cost_matrix = temp_spo2[temp_spo2['cost_all'] > 0]

        cost_matrix1 = cost_matrix[cost_matrix['cost_all'] > 0]
        cost_all = cost_matrix1['cost_all'].mean()
        cost_all = float('%.1f' % cost_all)
        h = '平均耗时:' + str(cost_all) + 's'

    else:
        train_x_list = []
        train_y_list = []
        train_z_list = []
        train_e_list = []
        train_r_list = []
        train_k_list = []
        dd = []
        h = '平均耗时:' + str(0) + 's'

    if len(dd) >= 10:
        h1 = Error_pro(date_pro)
    else:
        h1 = ''

    start, end = Choose_time(checklist)
    plotstr = str(date_pro) + '/' + username + '-'+title + ': ' + 'The useful data rate is ' + str(rate_all) +'% 晚间(' + str(end) + ':00--' + str(start) + ':00)有效率：' +str(rate_night1) +  '% ; 白天 ：' + str(rate_day1) + '%)'
    line = Scatter("血氧/心率值",plotstr,title_top="0%")
    line.add("血氧", train_x_list, train_y_list, xaxis_min=0, xaxis_max=24,legend_top="1%")
    line.add("心率", train_x_list, train_z_list, xaxis_min=0, xaxis_max=24,legend_top="1%")
    line.add("信号不佳", train_r_list, train_e_list, xaxis_min=0, xaxis_max=24,legend_top="1%")

    line.xaxis_min = 0
    line.xaxis_max = 24



    if len(temp_spo2) < 144:
        train_t_list,train_w_list = fill_data(temp_spo2,'cost')
        train_t_list,train_j_list = fill_data(temp_spo2,'cost_all')
        train_f_list, train_h_list = fill_data(temp_spo2, 'cost_cnt')
    else:
        train_w_list = data_to_list_spo2(temp_spo2, 'cost')
        train_h_list = data_to_list_spo2(temp_spo2, 'cost_cnt')
        train_j_list = data_to_list_spo2(temp_spo2, 'cost_all')


    line1 = Scatter("佩戴状态",h1,title_top="25%")
    line1.add("佩戴状态", train_x_list, train_k_list , xaxis_min = 0,xaxis_max = 24,legend_top="26%")

    bar = Bar("每次计算耗时",title_top="45%")
    bar.add("时长/s", train_t_list, train_w_list,yaxis_max = 100 ,yaxis_min = 0,is_datazoom_show=True, datazoom_xaxis_index=[2, 2],legend_top="45%")


    bar1 = Bar("计算总耗时",h,title_top="62%")
    bar1.add("总时长/s", train_t_list, train_j_list,yaxis_min = 0,legend_top="65%")

    bar2 = Bar("计算次数",title_top="83%")
    bar2.add("总次数",train_t_list, train_h_list,yaxis_min = 0,legend_top="85%")


    grid = Grid()
    grid.add(line, grid_bottom="78%")
    grid.add(line1, grid_top="31%", grid_bottom="58%")
    grid.add(bar, grid_top="50%", grid_bottom="40%")
    grid.add(bar1, grid_top="68%", grid_bottom="20%")
    grid.add(bar2, grid_top="88%", grid_bottom="2%")

    grid.renderer = 'svg'
    return grid


"""指定日期从网页爬取数据"""
def  Scrapy(str_date1,str_date2):
    global username
    global str_path

    pydata = {'export_wear': '导出16428数据',
              'filter_start_date': '2018-03-15',
              'filter_to_date': '2018-03-15'}
    str_CCID = '导出' + username + '数据'

    pydata['export_wear'] = str_CCID
    pydata['filter_start_date'] = str_date2
    pydata['filter_to_date'] = str_date1

    path = str_path + username

    df = []
    try:
        if str_path == str_path1:
            r=requests.post(path,headers = headers,data =pydata)
        else:
            r = requests.post(path, data=pydata)
    except requests.ConnectionError:
        a = 1
    else:
        imgBuf = StringIO(r.text)
        df = pd.read_csv(imgBuf)

    return df






def get3():
    global listname
    listname = Name_list()

def get4():
    global title
    title = Name_title()

da = []
def Data_get():
    global username
    global date_pro
    global slee
    global rate_all
    global rate_night1
    global rate_day1
    global title
    global listname
    global checklist
    global da

    TimeString = str(date_pro) + ' ' + '0:00:00'
    TimeStampChoose = int(time.mktime(time.strptime(TimeString, '%Y-%m-%d %H:%M:%S')))

    x = time.localtime(TimeStampChoose)  # localtime参数为float类型，这里y1317091800.0为float类型
    x2 = time.localtime(TimeStampChoose - 86400)
    str_date1 = time.strftime('%Y-%m-%d', x)
    str_date2 = time.strftime('%Y-%m-%d', x2)

    df = Scrapy(str_date1, str_date2)

    if len(df) < 8:
        da = []
    else:
        da = df.sort_values(axis=0, ascending=True, by='timestamp')
        sl = da[da['timestamp'] >= (TimeStampChoose - 10800)]
        sl = sl[sl['timestamp'] <= (TimeStampChoose + 32400)]
        sl.index = np.arange(len(sl))

        legnt4 = len(sl)
        slee = pd.DataFrame(np.arange(legnt4), columns=['ti'])
        slee['ti'] = 0
        slee['time'] = sl['timestamp'].map(Str_Change_Time(0))
        slee['wear_type'] = sl['wear_type']

        slee['ti'] = sl['sleep_effective_time'].diff()
        slee.loc[0, 'ti'] = 0
        slee['ti'] = slee['ti'].map(abs_diff)

        data_wear = da[da['wear_type'] == 1]

        da = da[da['timestamp'] >= TimeStampChoose]

        threads = []
        loops = [4, 2]
        nloops = range(len(loops))  # 列表[0,1]

        length_3 = len(da)

        if length_3 >= 2:
            # 创建线程
            t2 = threading.Thread(target=get3(), args=(0, loops[0]))
            threads.append(t2)

            t3 = threading.Thread(target=get4(), args=(0, loops[1]))
            threads.append(t3)

            # 开始线程
            for i in nloops:
                threads[i].start()

            # 等待所有结束线程
            for i in nloops:
                threads[i].join()

            if len(data_wear) >= 1:
                rate_all, rate_night1, rate_day1 = Com_Rate(data_wear,checklist)
        else:
            title = '--'



"""测试和运营/仿真平台的切换"""
def Data_Acquire():
    global da
    global name
    global str_path
    global title
    global username
    global list_flag
    cnt = 0
    Data_get()

    length_3 = len(da)
    while length_3 <= 0:
        if name == 0:
            str_path = str_path2
            list_flag = 0
            name = 1
        elif name == 1:
            str_path = str_path1
            list_flag = 0
            name = 2
        else:
            str_path = str_path3
            list_flag = 0
            name = 0
        Data_get()

        cnt = cnt + 1
        if cnt <= 2:
            length_3 = len(da)
        else:
            length_3 = 10



"""睡眠数据页面的图形绘制"""
def create_simple_pie():
    global slee

    data_m = slee['time']
    train_data_m = np.array(data_m)
    train_t_list = train_data_m.tolist()  # list

    data_m = slee['ti']
    train_data_m = np.array(data_m)
    train_w_list = train_data_m.tolist()  # list

    slee['ti'] = slee['ti'] *0.85
    data_m = slee['ti']
    train_data_m = np.array(data_m)
    train_l_list = train_data_m.tolist()  # list


    data_m = slee['wear_type']
    train_data_m = np.array(data_m)
    train_k_list = train_data_m.tolist()  # list

    bar = Bar("睡眠数据",'有效时长：',height=360)
    bar.add("时长/s", train_t_list, train_w_list,yaxis_max = 20 ,yaxis_min = 0,bar_category_gap=-10,legend_top="5%")
    #bar.add("校正后/s", train_t_list, train_l_list, yaxis_max=20, yaxis_min=0,bar_category_gap=-20,legend_top="5%")

    bar1 = Bar("佩戴状态",title_top="35%")
    bar1.add("佩戴状态", train_t_list, train_k_list,legend_top="35%",bar_category_gap = 0)

    grid = Grid()
    grid.add(bar, grid_top="10%",grid_bottom="70%")
    grid.add(bar1, grid_top="40%",grid_bottom="35%")

    grid.renderer = 'svg'
    return grid



"""统计数据的获取并绘制"""
def  Data_for_static():
    global username
    global date_pro
    global name
    global str_path
    global rate_save
    global day
    global temp_static
    global checklist

    year = int(str(date_pro)[0:4])
    month = int(str(date_pro)[5:7])
    day = int(str(date_pro)[8:10])
    lastDay = getMonthFirstDayAndLastDay(year,month)
    str_date2 = str(year)+ '-' + str(month)+'-' + str(1)
    str_date1 = str(year)+ '-' + str(month)+'-' + str(lastDay)


    if len(rate_save) > 15 and rate_save.iloc[0,4] == username and rate_save.iloc[1,4] == month and day == rate_save.iloc[2,4]:
        rate_save['username'] = username
    else:
        if len(rate_save) > 15 and rate_save.iloc[0, 4] == username and rate_save.iloc[1, 4] == month :
            rate_save['username'] = username
        else:
            cnt = 0
            while cnt <= 2:
                if name == 0:
                    str_path = str_path2
                    name = 1
                elif name == 1:
                    str_path = str_path1
                    name = 2
                else:
                    str_path = str_path3
                    name = 0

                if cnt <= 0:
                    temp_static = Scrapy(str_date1, str_date2)
                else:
                    df2 = Scrapy(str_date1, str_date2)
                    temp_static = pd.merge(temp_static, df2, how='outer')
                cnt = cnt + 1

            temp_static['date'] = temp_static['datetime'].map(Time_get(0))
            temp_static['Hour'] = temp_static['datetime'].map(Time_get(1))

            rate_save = pd.DataFrame(np.arange(lastDay+1), columns=['timesta'])
            rate_save['rate'] = 0
            rate_save['rate_night'] = 0
            rate_save['rate_day'] = 0
            rate_save['username'] = username
            rate_save.iloc[1,4] = month
            rate_save.iloc[2, 4] = day

        start,end = Choose_time(checklist)

        for i in range(lastDay):
            da = temp_static[temp_static['date'] == i]

            data = da[da['wear_type'] == 1]

            rate = Get_rate(data)

            data_night1 = data[data['Hour'] <= start]
            data_night2 = data[data['Hour'] >= end]
            data_night = pd.merge(data_night1, data_night2, how='outer')
            rate_night = Get_rate(data_night)

            data_day = data[data['Hour'] > start]
            data_day = data_day[data_day['Hour'] < end]
            rate_day = Get_rate(data_day)

            rate_save.iloc[i, 0] = i
            rate_save.iloc[i, 1] = rate
            rate_save.iloc[i, 2] = rate_night
            rate_save.iloc[i, 3] = rate_day

    rate1 = rate_save[rate_save['rate'] > 0]['rate'].mean()
    rate1 = float('%.2f' % rate1)
    rate2 = rate_save[rate_save['rate_night'] > 0]['rate_night'].mean()
    rate2 = float('%.2f' % rate2)
    rate3 = rate_save[rate_save['rate_day'] > 0]['rate_day'].mean()
    rate3 = float('%.2f' % rate3)

    data_m = rate_save['timesta']
    train_data_m = np.array(data_m)
    train_k_list = train_data_m.tolist()  # list

    data_m = rate_save['rate']
    train_data_m = np.array(data_m)
    train_l_list = train_data_m.tolist()  # list

    data_m = rate_save['rate_night']
    train_data_m = np.array(data_m)
    train_m_list = train_data_m.tolist()  # list


    data_m = rate_save['rate_day']
    train_data_m = np.array(data_m)
    train_n_list = train_data_m.tolist()  # list


    strplot =  '数据有效率：' + str(rate1) + '% 晚间(' + str(end) +':00--'+ str(start)+ ':00)有效率：'+ str(rate2)+ '% 白天('+ str(start) + ':00--'+str(end) +':00)有效率：'+ str(rate3)  +'%'
    str1 = username + '-'+ title+ '--'+str(year) + '年' + str(month) + '月' + '  ' + strplot

    bar = Bar("数据有效率统计(%)",str1)
    bar.add("有效率/%", train_k_list, train_l_list,xaxis_min = 1,legend_top="5%")


    bar1 = Bar("晚间数据有效率统计(%)",title_top="30%")
    bar1.add("rate_night/%", train_k_list, train_m_list,xaxis_min = 1,legend_top="30%")
    bar1.add("rate_day/%", train_k_list, train_n_list,xaxis_min = 1,legend_top="30%")


    bar2 = Bar("白天数据有效率统计(%)",title_top="55%")
    bar2.add("rate_day /%", train_k_list, train_n_list,xaxis_min = 1,legend_top="55%")

    grid = Grid()

    grid.add(bar, grid_top="10%",grid_bottom="75%")
    grid.add(bar1, grid_top="35%",grid_bottom="50%")
    grid.add(bar2, grid_top="60%", grid_bottom="25%")

    grid.renderer = 'svg'
    return grid




def   Error_pro(date_pro):

    h1 = '血氧灯模块错误'

    TimeString = str(date_pro) + ' ' + '0:00:00'
    TimeStampChoose = int(time.mktime(time.strptime(TimeString, '%Y-%m-%d %H:%M:%S')))

    x = time.localtime(TimeStampChoose + 86400)  # localtime参数为float类型，这里y1317091800.0为float类型
    x2 = time.localtime(TimeStampChoose - 86400 * 5)
    str_date1 = time.strftime('%Y-%m-%d', x)
    str_date2 = time.strftime('%Y-%m-%d', x2)

    l1 = Scrapy(str_date1, str_date2)
    length_all = len(l1)
    l1 = l1[l1['healthindex'] == 217]
    bad = len(l1)
    ra = bad / length_all


    length = len(l1)
    temp1 = pd.DataFrame(np.arange(length), columns=['wear_data'])
    temp1['wear_data'] = l1['wear_data'].map(Str_Chage_N(14))
    temp2 = pd.DataFrame(np.arange(length), columns=['wear_data'])
    temp2['wear_data'] = l1['wear_data'].map(Str_Chage_N(12))
    temp3 = pd.merge(temp1, temp2, how='outer')

    temp_mean = temp3['wear_data'].mean()

    if ra <= 0.3:
        h2 = ':请客户继续佩戴,便于分析'
    else:
        h2 = '：请客户直接寄回维修！'
    if temp_mean <= 5:
        h2 = h2 + 'FPC连接异常'
    h1 = h1 + h2 + str(bad) + '/' + str(length_all)

    return h1



