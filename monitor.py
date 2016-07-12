#!/usr/bin/python
# encoding=utf-8
import os
import signal
import subprocess
import time
import smtplib
import random
from email.mime.text import MIMEText
from email.header import Header

stoptime = time.strftime('%Y-%m-%d', time.localtime(time.time() + 10))
log_path = '/phpstudy/log/www/wmsadminapi/'
log_files =[
    ["grep -rn 'error_code'", log_path, "Api"+ '.' + stoptime + '*.log',  log_path+"Api_monitor"+ '.' + stoptime + '.log', ['312493732@qq.com']],
    ["grep -rn 'error_code'", log_path, "basic"+ '.' + stoptime + '*.log', log_path+"basic_monitor"+ '.' + stoptime + '.log', []],
    ["grep -rn 'error'", log_path, "production"+ '.' + stoptime + '*.log', log_path+"production_monitor"+ '.' + stoptime + '.log', []],
    ["grep -rn 'error'", log_path, "Stocktake"+ '.' + stoptime + '*.log', log_path+"Stocktake_monitor"+ '.' + stoptime + '.log', []]
 ]

mail_config = [
    ['smtp.sina.cn', 'caroltc@sina.cn', '******'],
    ['smtp.sina.cn', 'caroltc@sina.cn', '******']
]
default_receivers = ['ctang1@ibenben.com']  # default接收邮件

def monitorLog(find_key, log_path, log_file_name, monitor_file, receivers):
    log_file = log_path+log_file_name
    print '监控的日志文件 %s' % log_file
    popen = subprocess.Popen(find_key+' ' + log_file, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    pid = popen.pid
    if not os.path.exists(monitor_file):
        f=file(monitor_file, 'w')
        f.write('0')
        f.close()
    store_f=open(monitor_file,"r")
    line_str = store_f.readline()
    if line_str.strip() == '':
        store_nums = 0
    else :
        store_nums = int(line_str)
    lines = popen.stdout.readlines()
    now_nums = len(lines)
    print('Popen.pid:' + str(pid) + ' store_nums:'+str(store_nums)+' now_nums:' + str(now_nums))
    content = ''
    if now_nums > store_nums :
        for i in range(store_nums , now_nums):
            content = content + "\n" +lines[i]
        try:
            sendMail(str(now_nums - store_nums)+' errors in '+log_file_name, content, receivers)
        except Exception,e:
            print(str(e))
            popen.kill()
            return 0
    f=open(monitor_file, 'w')
    f.write(str(now_nums))
    f.close()
    popen.kill()

def sendMail(subject, content, receivers):
    mail_info = mail_config[random.randint(0, (len(mail_config)-1))]
    mail_host = mail_info[0]
    mail_user = mail_info[1]
    mail_pass = mail_info[2]
    message = MIMEText(content, 'plain', 'utf-8')
 #   message['From'] = Header(mail_user, 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')    
    try:
        smtpObj = smtplib.SMTP() 
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)  
        smtpObj.sendmail(mail_user, receivers, message.as_string())
        print "邮件发送成功"
    except Exception,e:
        print "Error: 无法发送邮件"
        print(str(e))
        raise Exception("SendMail Error")

if __name__ == '__main__':
    for log_file in (log_files):
        mail_receivers = default_receivers + log_file[4]
        monitorLog(log_file[0], log_file[1], log_file[2], log_file[3], mail_receivers)
        time.sleep(3)

