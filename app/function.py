import asyncio
from telegram import Bot
from datetime import datetime
from user_agents import parse
from django.conf import settings
from .models import AccessRecord

def output_page_line_notify(request,request_url):
    access_time=datetime.now()
    year=access_time.year
    month=access_time.month
    day=access_time.day
    hour=access_time.hour
    minute=access_time.minute
    second=access_time.second
    if request_url=="output":
        asyncio.run(send_notify(f"已於 {year}/{month}/{day} {hour}:{minute}:{second} 開啟"))
    elif request_url=="outputOff":
        asyncio.run(send_notify(f"已於 {year}/{month}/{day} {hour}:{minute}:{second} 關閉"))
    else:
        print("Send Notify Error")
#LINE Notify
"""
def send_notify(message):
    line_notify_token = settings.LINE_NOTIFY_TOKEN
    url="https://notify-api.line.me/api/notify"
    headers={"Authorization": f"Bearer {line_notify_token}"}
    data={"message": message}
    response=requests.post(url, headers=headers, data=data)
    if response.status_code==200:
        print("Send Line Notify Success")
    else:
        print("Send Line Notify Error")
"""
#Telegram Notify BY requests package
"""
def send_notify(message):
    bot_token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, data=payload)
    return response.json()
"""

async def send_notify(message):
    bot_token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=message)

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

def get_client_ip(request):
    x_forwarded_for=request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip=x_forwarded_for.split(',')[0]
    else:
        ip=request.META.get('REMOTE_ADDR')
    return ip
