# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 18:06:55 2018

@author: Administrator
"""

from email import encoders  
import os  
import traceback  
from email.header import Header  
from email.mime.text import MIMEText  
from email.utils import parseaddr, formataddr  
import smtplib  
from email.mime.multipart import MIMEMultipart  
from email.mime.base import MIMEBase  
from email import encoders  
  
  
# 中文处理  
def _format_addr(s):  
    name, addr = parseaddr(s)  
    return formataddr((Header(name, 'utf-8').encode(), addr))  
  
def send_email(to_addr_in,filepath_in):  
    # 邮件发送和接收人配置  
    global r
    global filepath
    from_addr = '573501957@qq.com'  
    smtp_server = 'smtp.qq.com'  
    password = 'pqsqifufqwagbdia'  
    to_addr = to_addr_in  
    to_addrs = to_addr.split(',')  
  
    msg = MIMEMultipart()  
    msg['From'] = _format_addr('久乐佩戴数据分析平台 <%s>' % from_addr)        # 显示的发件人  
    # msg['To'] = _format_addr('管理员 <%s>' % to_addr)                # 单个显示的收件人  
    msg['To'] = ",".join(to_addrs)                                    # 多个显示的收件人  
    msg['Subject'] = Header('硬件故障列表', 'utf-8').encode()      # 显示的邮件标题  
  
    # 需要传入的路径  
    # filepath = r'D:\test'  
    filepath = filepath_in  
    r = os.path.exists(filepath)  
    if r is False:  
        msg.attach(MIMEText('no file...', 'plain', 'utf-8'))  
    else:  
        # 邮件正文是MIMEText:  
        msg.attach(MIMEText('故障诊断列表见附件，请查收...', 'plain', 'utf-8'))  
        # 遍历指定目录，显示目录下的所有文件名  
        pathDir = os.listdir(filepath)  
        for allDir in pathDir:  
            child = os.path.join(filepath, allDir)  
  
            # 添加附件就是加上一个MIMEBase，从本地读取一个文件  
            with open(child, 'rb') as f:  
                # 设置附件的MIME和文件名，这里是txt类型:  
                mime = MIMEBase('file', 'xls', filename=allDir)  
                # 加上必要的头信息:  
                mime.add_header('Content-Disposition', 'attachment', filename=allDir)  
                mime.add_header('Content-ID', '<0>')  
                mime.add_header('X-Attachment-Id', '0')  
                # 把附件的内容读进来:  
                mime.set_payload(f.read())  
                # 用Base64编码:  
                encoders.encode_base64(mime)  
                # 添加到MIMEMultipart:  
                msg.attach(mime)  
    try:  
        server = smtplib.SMTP_SSL(smtp_server, 465) 
        server.set_debuglevel(1)  # 用于显示邮件发送的执行步骤  
        server.login(from_addr, password)  
        server.sendmail(from_addr, to_addrs, msg.as_string())  
        server.sendmail(from_addr, '573501957@qq.com', msg.as_string())  
        server.quit()  
    except Exception:  
        print ("Error: unable to send email")  
        print (traceback.format_exc() ) 
        
#send_email('573501957@qq.com','D:\\data\\myself\\test')        
#send_email('hwang@jiuletech.com','D:\\data\\myself\\test')  