import requests
from datetime import datetime
from user_agents import parse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings
from .models import AccessRecord
#import os
#import openpyxl
#import subprocess
#import time
#from django.utils import timezone

def output_page_line_notify(request,request_url):
    access_time=datetime.now()
    year=access_time.year
    month=access_time.month
    day=access_time.day
    hour=access_time.hour
    minute=access_time.minute
    second=access_time.second
    if request_url=="output":
        send_line_notify(f"已於 {year}/{month}/{day} {hour}:{minute}:{second} 開啟")
    elif request_url=="outputOff":
        send_line_notify(f"已於 {year}/{month}/{day} {hour}:{minute}:{second} 關閉")
    elif request_url=="ultrasound":
        send_line_notify(f"已於 {year}/{month}/{day} {hour}:{minute}:{second} 接收到超聲波異常，請到後臺檢查")
    elif request_url == "output2":
        send_line_notify(f"已於 {year}/{month}/{day} {hour}:{minute}:{second} 開啟")
    elif request_url == "outputOff2":
        send_line_notify(f"已於 {year}/{month}/{day} {hour}:{minute}:{second} 關閉")
    elif request_url == "ultrasound2":
        send_line_notify(f"已於 {year}/{month}/{day} {hour}:{minute}:{second} 接收到超聲波異常，請到後臺檢查")

    else:
        print("output_page_line_notify Error")


def handle_common_logic(request,request_urls):
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    user_agent_info = parse(user_agent)
    os_info = user_agent_info.os
    os_name = os_info.family
    os_version = os_info.version_string
    browser_info = user_agent_info.browser
    browser_name = browser_info.family
    browser_version = browser_info.version_string
    record_access_time(request, os_name, os_version, browser_name, browser_version,request_urls)



def record_access_time(request, os_name, os_version, browser_name, browser_version, request_urls):
    ip_address = request.META.get('REMOTE_ADDR')
    access_record = AccessRecord.objects.create(
        ip_address=ip_address,
        urls=request_urls,
        os_name=os_name,
        os_version=os_version,
        browser_name=browser_name,
        browser_version=browser_version
    )
    #print(f"Access Time {access_record.access_time} recorded successfully.")


"""
#To Excel
def record_access_time(request, os_name, os_version, browser_name, browser_version, request_urls):
    media_root = settings.MEDIA_ROOT
    excel_file = os.path.join(media_root, "access_log.xlsx")
    access_time = datetime.now()
    year = access_time.year
    month = access_time.month
    day = access_time.day
    hour = access_time.hour
    minute = access_time.minute
    second = access_time.second
    sheet_name = f"{year}年{month}月"
    try:
        wb = openpyxl.load_workbook(excel_file)
    except FileNotFoundError:
        wb = openpyxl.Workbook()
    if sheet_name not in wb.sheetnames:
        sheet = wb.create_sheet(sheet_name)
        sheet.append(["Year", "MM/DD", "H/M/S", "IP", "Urls", "OS Name", "OS Ver", "Browser Name", "Browser Ver"])
    sheet = wb[sheet_name]
    ip_address = request.META.get('REMOTE_ADDR')
    urls = request_urls
    month_day = f"{month}/{day}"
    hour_min_sec = f"{hour:02d}:{minute:02d}:{second:02d}"
    sheet.append([year, month_day, hour_min_sec, ip_address, urls, os_name, os_version, browser_name, browser_version])
    wb.save(excel_file)
    print(f"Access Time {access_time} Success Record To {sheet_name}")
"""
def get_client_ip(request):
    x_forwarded_for=request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip=x_forwarded_for.split(',')[0]
    else:
        ip=request.META.get('REMOTE_ADDR')
    return ip

def send_line_notify(message):
    line_notify_token = settings.LINE_NOTIFY_TOKEN
    url="https://notify-api.line.me/api/notify"
    headers={"Authorization": f"Bearer {line_notify_token}"}
    data={"message": message}
    response=requests.post(url, headers=headers, data=data)
    if response.status_code==200:
        print("Send Line Notify Success")
    else:
        print("Send Line Notify Error")

def send_smtp(public_url):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = "kenchoustudio@gmail.com"
    smtp_password=settings.SMTP_PASSWORD
    sender_email = "kenchoustudio@gmail.com"
    receiver_email = "kenchoustudio@gmail.com"
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Django Server"
    message.attach(MIMEText(public_url))
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("Send Mail Success")
    except Exception as e:
        print(f"Send Mail Error: {str(e)}")