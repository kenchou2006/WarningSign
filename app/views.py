from django.shortcuts import render,redirect
from django.http import HttpResponseNotFound, HttpResponse ,HttpResponseRedirect,JsonResponse
import os
import json
import socket
import asyncio
from django.core.cache import cache
from app.function import handle_common_logic,record_access_time,get_client_ip,output_page_line_notify,send_notify
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.core.cache import cache
from .models import AccessRecord

input_visited=False
input_off_visited=False
output_status=False
output_off_status=False
arduino_online=False

waringsign_status=2
arduino_battery_num=0

arduino_charing=2
arduino_eco=2

line_notify_arduino_status_UltraSound=True
notify_battery=True

request_url="Other"

input_visited2=False
input_off_visited2=False
output_status2=False
output_off_status2=False
waringsign_status2=False
arduino_online2=False
arduino_status_UltraSound2=True
arduino_battery_num2=0
arduino_battery_tem2=0
line_notify_arduino_status_UltraSound2=True

def index(request):
    if request.user.is_authenticated:
        Account = request.user
    else:
        Account = None
    context = {
        'Account': Account,
    }
    return render(request, 'index.html', context)

def Sign1(request):
    global arduino_battery_num, waringsign_status, arduino_charing, arduino_eco
    if request.user.is_authenticated:
        Account = request.user
    else:
        Account = None
    output_visited = cache.get('output_visited')
    if waringsign_status == 1:
        waringsign_status_view = True
    else:
        waringsign_status_view = False

    if arduino_charing == 1:
        arduino_charing_view = True
    else:
        arduino_charing_view = False

    if arduino_eco == 1:
        arduino_eco_view = True
    else:
        arduino_eco_view = False

    if output_visited:
        arduino_online = True
    else:
        arduino_online = False
    context = {
        'Account': Account,
        'output_status': input_visited,
        'waringsign_status': waringsign_status_view,
        'output_off_status': input_off_visited,
        'arduino_online': arduino_online,
        'arduino_battery_num': arduino_battery_num,
        'arduino_charing': arduino_charing_view,
        'arduino_eco': arduino_eco_view,
    }
    return render(request, 'sign1.html', context)


@csrf_exempt
def arduino_info(request):
    global arduino_battery_num, waringsign_status, arduino_status_UltraSound, line_notify_arduino_status_UltraSound,arduino_charing, arduino_eco, notify_battery
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            def parse_int(value, default=0):
                try:
                    return int(value)
                except (ValueError, TypeError):
                    return default
            arduino_battery_num = parse_int(data.get('battery', 0))
            waringsign_status_str = parse_int(data.get('waringsign_status', 2))
            arduino_charing_str = parse_int(data.get('charing', 2))
            arduino_eco_str = parse_int(data.get('eco', 2))

            if waringsign_status_str == 1:
                waringsign_status = 1
                waringsign_status_input = True
            elif waringsign_status_str == 2:
                waringsign_status = 2
                waringsign_status_input = True
            else:
                waringsign_status_input = False

            if arduino_charing_str == 1:
                arduino_charing = True
            else:
                arduino_charing = False

            if arduino_eco_str == 1:
                arduino_eco = True
            else:
                arduino_eco = False

            if arduino_battery_num <= 20 and notify_battery:
                notify_battery = False
                asyncio.run(send_notify("電量低於 20，請檢查狀態"))
            elif not arduino_battery_num <= 20:
                notify_battery = True

            if waringsign_status_input:
                return JsonResponse({"status": "success"})
            else:
                return JsonResponse({"status": "error", "message": "Invalid data"})

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON data"})
    else:
        return JsonResponse({"status": "error", "message": "Invalid method"})

def cleanCache(request):
    global arduino_battery_num, waringsign_status, line_notify_arduino_status_UltraSound, arduino_charing, arduino_eco, notify_battery,input_visited,input_off_visited,output_status,output_off_status,arduino_online,arduino_battery_num,request_url
    global input_visited2,input_off_visited2,output_status2,output_off_status2,waringsign_status2,arduino_online2,arduino_status_UltraSound2,arduino_battery_num2,arduino_battery_tem2,line_notify_arduino_status_UltraSound2
    if request.user.is_authenticated:
        input_visited = False
        input_off_visited = False
        output_status = False
        output_off_status = False
        arduino_online = False
        waringsign_status = 2
        arduino_battery_num = 0
        arduino_charing = 2
        arduino_eco = 2
        line_notify_arduino_status_UltraSound = True
        notify_battery = True
        request_url = "Other"
        input_visited2 = False
        input_off_visited2 = False
        output_status2 = False
        output_off_status2 = False
        waringsign_status2 = False
        arduino_online2 = False
        arduino_status_UltraSound2 = True
        arduino_battery_num2 = 0
        arduino_battery_tem2 = 0
        line_notify_arduino_status_UltraSound2 = True
        return HttpResponseRedirect('/sign1')
    else:
        return HttpResponseRedirect('/')


def input_page(request):
    global output_status, input_visited, request_url
    request_url = "input"
    if not input_visited:
        handle_common_logic(request, request_url),
        if not input_visited:
            output_status = True
            input_visited = True
        if request.user.is_authenticated:
            return HttpResponseRedirect('/sign1')
        else:
            return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})

def input_off_page(request):
    global output_off_status, input_off_visited,request_url
    request_url="inputOff"
    handle_common_logic(request, request_url)

    if not input_off_visited:
        output_off_status=True
        input_off_visited=True
        output_page_line_notify(request, request_url)
        return HttpResponseRedirect('/sign1')
    else:
        return HttpResponseNotFound("Error")


def output_page(request):
    global output_status, input_visited, request_url
    request_url = "output"
    cache.set('output_visited', True, 30)

    if input_visited:
        output_status = True
        input_visited = False
        handle_common_logic(request, request_url)
        output_page_line_notify(request, request_url)

    else:
        output_status = False

    if output_status:
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})


def output_off_page(request):
    global output_off_status, input_off_visited,request_url
    request_url = "outputOff"
    cache.set('output_visited', True, 30)
    if input_off_visited:
        output_off_status=True
        input_off_visited=False
        handle_common_logic(request, request_url),
        output_page_line_notify(request, request_url)
    else:
        output_off_status=False
    if output_off_status:
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})

def Sign2(request):
    global arduino_battery_num2,arduino_battery_tem2,waringsign_status2,arduino_status_UltraSound2
    if request.user.is_authenticated:
        Account=request.user
    else:
        Account=None
    output_visited2 = cache.get('output_visited2')
    if output_visited2:
        arduino_online2=True
    else:
        arduino_online2=False
    context = {
        'Account':Account,
        'output_status':input_visited2,
        'waringsign_status':waringsign_status2,
        'output_off_status':input_off_visited2,
        'arduino_status_UltraSound':arduino_status_UltraSound2,
        'arduino_online':arduino_online2,
        'arduino_battery_num': arduino_battery_num2,
        'arduino_battery_tem':arduino_battery_tem2,
    }
    return render(request,'sign2.html',context)

def arduino_info2(request):
    global arduino_battery_num2,arduino_battery_tem2,waringsign_status2,arduino_status_UltraSound2
    global line_notify_arduino_status_UltraSound2
    arduino_battery_num2 = int(request.GET.get('url_battery', 0))
    arduino_battery_tem2 = int(request.GET.get('url_battery_tem', 0))
    print("==========================================================================")
    print(f"arduino_battery_num:{arduino_battery_num2}")
    print(f"arduino_battery_tem:{arduino_battery_tem2}")
    waringsign_status_str2 = request.GET.get('url_waringsign_status')
    if waringsign_status_str2 == '1':
        waringsign_status2 = True
        print(f"waringsign_status:{waringsign_status2}")
    elif waringsign_status_str2 == '2':
        waringsign_status2 = False
        print(f"waringsign_status:{waringsign_status2}")
    else:
        print(f"waringsign_status_str:{waringsign_status_str2}")
    arduino_status_UltraSound_str2 = request.GET.get('url_UltraSound')
    if arduino_status_UltraSound_str2 == '1':
        arduino_status_UltraSound2 = True
        line_notify_arduino_status_UltraSound2 = True
        print(f"arduino_status_UltraSound:{arduino_status_UltraSound2}")
    elif arduino_status_UltraSound_str2 == '2':
        arduino_status_UltraSound2 = False
        request_url="ultrasound2"
        if line_notify_arduino_status_UltraSound2 == True:
            output_page_line_notify(request, request_url)
            line_notify_arduino_status_UltraSound2 = False
        print(f"arduino_status_UltraSound:{arduino_status_UltraSound2}")
    else:
        print(f"arduino_status_UltraSound_str:{arduino_status_UltraSound_str2}")
    print("==========================================================================")
    return HttpResponse("Success")

def input_page2(request):
    if request.user.is_authenticated:
        global output_status2,input_visited2,request_url
        request_url = "input2"
        if not input_visited2:
            handle_common_logic(request,request_url)
            if not input_visited2:
                output_status2=True
                input_visited2=True
            return HttpResponseRedirect('/sign2')
        else:
            return HttpResponseNotFound("Error")
    else:
        return HttpResponseRedirect('/')

def input_off_page2(request):
    global output_off_status2, input_off_visited2,request_url
    request_url="inputOff2"
    handle_common_logic(request,request_url)
    if not input_off_visited2:
        output_off_status2=True
        input_off_visited2=True
        output_page_line_notify(request, request_url)
        return HttpResponseRedirect('/sign2')
    else:
        return HttpResponseNotFound("Error")

def output_page2(request):
    global output_status2,input_visited2,request_url
    request_url = "output2"
    cache.set('output_visited2', True, 30)
    if input_visited2:
        output_status2=True
        input_visited2=False
        handle_common_logic(request,request_url)
        output_page_line_notify(request,request_url)
    else:
        output_status2=False
    if output_status2:
        return HttpResponseRedirect('/sign2')
    else:
        return HttpResponseNotFound("Error")


def output_off_page2(request):
    global output_off_status2, input_off_visited2,request_url
    request_url = "outputOff2"
    cache.set('output_visited2', True, 30)
    if input_off_visited2:
        output_off_status2=True
        input_off_visited2=False
        output_page_line_notify(request,request_url)
        handle_common_logic(request, request_url)
    else:
        output_off_status2=False
    if output_off_status2:
        return HttpResponseRedirect('/sign2')
    else:
        return HttpResponseNotFound("Error")
"""
def server_info(request):
    host_name=platform.node()
    os_name=platform.system()
    os_version=platform.release()
    processor=platform.processor()
    current_directory=os.getcwd()
    memory=psutil.virtual_memory()
    total_ram=memory.total
    internal_ipv4=socket.gethostbyname(socket.gethostname())
    context = {
        'host_name':host_name,
        'os_name':os_name,
        'os_version':os_version,
        'processor': processor,
        'current_directory':current_directory,
        'total_ram':total_ram,
        'internal_ipv4':internal_ipv4,}
    return render(request,'server_info.html',context)
"""
def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('/')  # 'home'是你的首页URL名称
        else:
            messages.error(request, 'Invalid login credentials.')
    return render(request, 'login.html')

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')
    else:
        return redirect('/')

def access_record_list(request):
    if request.user.is_authenticated:
        access_records = AccessRecord.objects.all()
        return render(request, 'access_record_list.html', {'access_records': access_records})
    else:
        return redirect('/')

def clear_access_records(request):
    if request.user.is_authenticated:
        AccessRecord.objects.all().delete()
        return redirect('access_record_list')
    else:
        return redirect('/')