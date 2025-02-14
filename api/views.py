from django.shortcuts import render
from django.http import JsonResponse
from app import views

def infoAPI(request):
    return JsonResponse({"battery": views.arduino_battery_num})