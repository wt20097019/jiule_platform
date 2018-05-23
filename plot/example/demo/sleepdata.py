# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 20:44:27 2018

@author: Administrator
"""


import pandas as pd
import numpy as np
from datetime import datetime,timedelta
import time
import re
import requests
from io import StringIO
from sendemail import send_email
from bs4 import BeautifulSoup as bs
import threading   
from time import sleep, ctime   


factory  = pd.read_csv('factory.csv')

t3_error = 0

def Change(str1):
    aa = float(re.findall(r"\d+\.?\d*",str1)[0])
    return aa

def Time_use(mm):
    strcu_time = time.strptime(mm, '%Y-%m-%d %H:%M:%S')
    if (strcu_time[4]%10 ) >=1  or strcu_time[5] >= 10:
        type = 0
    else:
        type = 1
    return type 

"""将字符串时间转换为float型"""
def Str_Change_time2(strchange):
    time_local = time.localtime(strchange)
    time_pro = time.localtime(strchange)
    if time_pro[3]+ time_pro[4]/60 > 0:
        data_value = time_pro[3] + time_pro[4]/60  
    else:
        data_value = time_pro[3] + time_pro[4]/60 + 0.01
    return data_value


def Str_Change_time3(strchange):
    time_pro = time.strptime(strchange, '%Y-%m-%d %H:%M:%S')
    if time_pro[3]+ time_pro[4]/60 > 0:
        data_value = time_pro[3] + time_pro[4]/60  
    else:
        data_value = time_pro[3] + time_pro[4]/60 + 0.01
    return data_value

def Str_Chage_N(n): 
    def str_change_in(strchange):
        if n >= 16:
            coe = 2
        else:
            coe = 4
        if len(strchange) >= n+2:
            data_value = int(strchange[n:n+2],16) * coe    
        else:
            data_value = 0
        if strchange[0:6] == '120816' and n == 14:
            data_value = 1
        return data_value
    return str_change_in


"""搜索睡眠数据并按照顺序排列"""
def Sleep_Rank(date_to):
    strpath =  'http://api.jiuletech.com/data/t3_sleep.php?page='  
    user = ''
    path =  strpath + str(1) +'&filter_date='+date_to + '&filter_name=' + user
    
    data =pd.read_html(path)[0]
    for i in range(10):  
        path =  strpath + str(i+1) +'&filter_date='+date_to + '&filter_name=' + user
        #读取网页中表格信息       
        data2 =pd.read_html(path)[0]
        time.sleep(1)
        length = len(data)
        if length > 2:
            data = pd.merge(data, data2, how='outer')
        else:
            break
    data = data.drop(0)
    data.index = np.arange(len(data))
    data['Sleep_time'] = data[4].map(Change)
    data = data.sort_values('Sleep_time',ascending = False)   
    return data



""""Error_list创建"""    
def Error_list(Username,timestr,error_type):
    
    errorlist = pd.read_csv('D:\\data\\myself\\test\\errorlist.csv')
    data =errorlist[ errorlist['ccid'] == Username]
    m=errorlist[ errorlist['ccid'] == Username].index.tolist()
    
    if len(data) >= 1:
        errorlist.loc[m[0],'time_cnt'] = errorlist.get_value(m[0],'time_cnt') + 1
        errorlist.loc[m[0],'timestamp'] = timestr
        a = 0
        
    else:
        data.loc[0,'ccid'] =  Username
        data.loc[0,'time_cnt'] =  1
        data.loc[0,'timestamp'] = timestr   
        data.loc[0,'error'] = error_type   
        errorlist = pd.merge(errorlist,data,how = 'outer')
        a = 1
        
    errorlist.to_csv('D:\\data\\myself\\test\\errorlist.csv',index=False)

    return a



def Error_Write(N,temp_user,date_to):
    global t3_error
    
    write_flag1 = Error_list(temp_user,date_to,N)
    if write_flag1 == 1 :              
        batch = factory[factory['ccid'] == temp_user]['batch']
        batch.index = np.arange(len(batch))
        
        if len(batch) >=1:
           bat = batch.get_value(0,'batch')
        else:
            bat = 0
        if N == 0:
            str4 = '故障类型为 多次重启，序列号为： ' + temp_user + '   批次为：'+ str(bat) +'\n'
        elif N==1:
            str4 = '故障类型为 血氧灯异常，序列号为： ' + temp_user + '   批次为：'+ str(bat) +'\n'
        else:
            str4 = '故障类型为 FPC连接不良，序列号为： ' + temp_user + '   批次为：'+ str(bat) +'\n'
           
        t3_error = t3_error + 1
        with open("D:\\data\\myself\\test\\error.txt","a") as f:
            f.write(str4)  
    

"""判断是否多次重启"""
def Error_Reset(date_to):
    global factory 
    strpath = 'http://api.jiuletech.com/data/t3_re_log.php?page='
    str1 = '&filter_name=&filter_type=07&filter_date='    
    
    path =  strpath + str(1) + str1 + date_to   
    data =pd.read_html(path)[0] 
    
    for i in range(1,100):  
        #time.sleep(1)
        path =  strpath + str(i+1) + str1 +date_to 
        #读取网页中表格信息  
        try:
            data2 =pd.read_html(path)[0]
            time.sleep(0.5)
        except requests.HTTPError:
            flag = flag +1
            
        else:
            length = len(data2)
            data = pd.merge(data, data2, how='outer')
            if length < 30:
                break
        
        if i%10 == 0:
            print('07下发指令读取中'+str(i))
            time.sleep(15)
            
    print('07下发指令读取完成'+str(i))
    data = data.drop(0)
       
    data1 = data[data[4]== '9000']
    data1['num'] = 1
    data3 = data1['num'].groupby(data1[1]).sum()
    data4 = data3[data3.values >= 20]
    length = len(data4)
    
    temp1 = pd.DataFrame(np.arange(length),columns = ['ccid'])
    temp1['ccid'] = data3[data3.values >= 20].index
    
    for i in range(len(temp1)):
        temp_user = temp1.get_value(i,'ccid')
        temp2 = data1[data1[1]==temp_user ]
        temp2.index = np.arange(len(temp2))
        temp2['time'] = temp2[5].map(Str_Change_time3)
        temp2['dela'] = 0
        
        for j in range(len(temp2)-1):
            temp2.loc[j,'dela'] = temp2.get_value(j,'time') -  temp2.get_value(j+1,'time')
               
        mean = temp2['dela'].mean()
        
        if mean >= 0.078  and mean <= 0.088:
            work1 = 1
        else:
             Error_Write(0,temp_user,date_to) 


        
"""读取健康数据并完成判断"""
def  Data_Process(data,date_to):
    global t3_error
    global t3 
    global sleep_length
    global factory
    global temp4

    strcu_time = time.strptime(date_to, '%Y-%m-%d')
    yesterday = datetime(strcu_time[0], strcu_time[1], strcu_time[2]) + timedelta(-1)  
    date_start = yesterday.strftime("%Y-%m-%d")
    
    pydata = {'export_wear':'导出16428数据',
      'filter_start_date':'2018-03-01',
      'filter_to_date':'2018-03-09'}
    
    str_path = 'http://api.jiuletech.com/data/t3_data.php?filter_name='
    
    sleep_length = len(data)
    
    for i in range(sleep_length):
        data.index = np.arange(len(data))
        UserName = data.get_value(i,0)
        path1 = str_path + UserName
        str_CCID = '导出'+UserName+'数据'
        pydata['export_wear'] = str_CCID
        pydata['filter_start_date'] = date_start
        pydata['filter_to_date'] = date_to
        #http://api.jiuletech.com/test/t3_data.php?page=5&filter_name=898600D6991600044300&s=1
        
            
        Num = data.get_value(i,'Sleep_time') * 2  
                        
        try:
            r=requests.post(path1,data =pydata)
            #time.sleep(1)
        except requests.ConnectionError:
            a = 1
        else:
            imgBuf = StringIO(r.text)
            df = pd.read_csv(imgBuf)
        mm = data.get_value(0,2)
        
        str_time = date_start + ' ' + mm
        time_pro1 = int(time.mktime(time.strptime(str_time, '%Y-%m-%d %H:%M')))
        
        mm = data.get_value(0,3)
        str_time = date_start + ' ' + mm
        time_pro2 = int(time.mktime(time.strptime(str_time, '%Y-%m-%d %H:%M'))) + 86400
        
        if len(df) > 20 :
            
            t3 = t3 + 1
            
            if Num >= 8:
                d1 = df[df['timestamp'] <= time_pro2]
                d1 = d1[d1['timestamp'] >= time_pro1]              
                d2 = d1[d1['spo2']+ d1['heartrate'] > 0]
                length = len(d2)
                
                if length <= Num:
                    
                    dm = d1[d1['wear_type'] == 1]
                    d3 = dm['datetime'].map(Time_use)
                    sum_bad = d3.sum()
                    if sum_bad >= 3:
                        #write_flag = 1
                        Error_Write(1,UserName,date_to) 
                    else:  
                        """
                        str4 = '佩戴出错   ' + UserName +'  ' +str(length)+'\n'
                        with open("D:\\data\\myself\\test\\error.txt","a") as f:
                            f.write(str4)  
                        """
                        
                        
            length = len(df)
            temp1 = pd.DataFrame(np.arange(length),columns = ['timestamp'])
            temp1['wear_data']= df['wear_data'].map(Str_Chage_N(14))
            temp2 = pd.DataFrame(np.arange(length),columns = ['timestamp'])
            temp2['wear_data']= df['wear_data'].map(Str_Chage_N(12))
            temp3 = pd.merge(temp1,temp2,how='outer')
            
            
            mean_wear = temp3[temp3['wear_data'] == 0]
            length = len(mean_wear)
            
            if UserName == '898600D6991600044300':
                temp4 = temp3
            
            if length >= 15:
                Error_Write(2,UserName,date_to)                                       
                            

                    
    if  t3 > 0:   
        error_rate = t3_error/t3 *100
    else:
        error_rate = 0
    str_error= 'T3手表共计'+ str(t3)+ '块'+',其中硬件故障率为：' +str(error_rate) + '%' + '\n'
    with open("D:\\data\\myself\\test\\error.txt","a") as f:
        f.write(str_error)  
    
 
def Write_error(date_to):
    global t3_error
    global t3
    global data_m
    print ('Start loopat:', ctime() )  
    ss = '------------------'+date_to+'----------------------'+'\n'
    with open("D:\\data\\myself\\test\\error.txt","w") as f:
        f.write(ss) 
    t3_error = 0
    t3 = 0
    data_m = Sleep_Rank(date_to) 
    #Error_Reset(date_to)  
    Data_Process(data_m,date_to)
    print ('All end:', ctime() )  
    
def main(date_to):  

    
    threads = []  
    loops = [4,2]   
    nloops = range(len(loops))     #列表[0,1]  
    
    print ('Start loopat:', ctime() )  
          
    #创建线程  
    t = threading.Thread(target=Write_error(date_to),args=(0,loops[0]))  
    threads.append(t)  
    
    t = threading.Thread(target=Error_Reset(date_to),args=(1,loops[1]))  
    threads.append(t)  
  
    #开始线程  
    for i in nloops:  
        threads[i].start()  
  
    #等待所有结束线程  
    for i in nloops:  
        threads[i].join()  
  
    print ('All end:', ctime() )  

def Sleep_By_Day(): 
    today=time.strftime('%Y-%m-%d',time.localtime(time.time()))
    week=int(time.strftime("%w"))
    date_to = today
      
    if week== 1:
        with open("D:\\data\\myself\\test\\error.txt","w") as f:
            f.write('') 
        

        strcu_time = time.strptime(date_to, '%Y-%m-%d')
        sun = datetime(strcu_time[0], strcu_time[1], strcu_time[2]) + timedelta(-1)  
        sun_str = sun.strftime("%Y-%m-%d")
        
        strcu_time = time.strptime(sun_str, '%Y-%m-%d')
        sat = datetime(strcu_time[0], strcu_time[1], strcu_time[2]) + timedelta(-1)  
        sat_str = sat.strftime("%Y-%m-%d")
        main(sat_str)
        time.sleep(2)        
        main(sun_str)
        time.sleep(2)
        
    main(date_to)    
    #Write_error(date_to)     
    return week
 
    

    

if __name__ == '__main__' :     
    week = Sleep_By_Day()   
    if t3_error >= 1:
        send_email('twang@jiuletech.com','D:\\data\\myself\\test')        
        #send_email('hwang@jiuletech.com','D:\\data\\myself\\test')  


