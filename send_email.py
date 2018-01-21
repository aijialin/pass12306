#!/usr/bin/python  
# -*- coding: utf-8 -*-  
import config

import smtplib  
from email.mime.text import MIMEText  
from email.mime.multipart import MIMEMultipart  
from email.header import Header  
import time 
  
def send(content):  
      
    #发送邮箱  
    mail_from = 'ticket_for_12306@qq.com'  
    #发送邮件主题  
    mail_subject = '已下单，请尽快登陆12306完成支付'
    #发送邮箱服务器  
    mail_smtpserver = 'smtp.qq.com'  
    #发送邮箱用户/密码  
    mail_username = config.mail_username
    mail_password = config.mail_password
  
    msg = MIMEText(content, 'plain', 'utf-8')
    #将邮件的主题等相关信息添加到邮件实例  
    msg['Subject'] = Header(mail_subject, "utf-8")  
    msg['From'] = "余票监控"
    msg['To'] = config.email
    msg['date'] = time.strftime('%a, %d %b %Y %H:%M:%S %z')   
    #创建发送服务器实例并将发送服务器添加到实例中  
    smtp = smtplib.SMTP()  

    smtp.connect(mail_smtpserver)
    smtp.starttls()

    #打印交互的日志信息 
    smtp.set_debuglevel(1) 
    
    #登录发送邮件服务器并进行邮件的发送  
    smtp.login(mail_username, mail_password)  
    smtp.sendmail(mail_from, config.email, msg.as_string())  
    
    smtp.quit()  
      
#send("同志你好，请尽快下单 https://kyfw.12306.cn/otn/queryOrder/initNoComplete")