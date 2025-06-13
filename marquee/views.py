from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate,login,logout

GLOBAL_MESSAGE = ""

def input_message(request):
    if request.user.is_authenticated:
        global GLOBAL_MESSAGE
        if request.method == "POST":
            GLOBAL_MESSAGE = request.POST.get("message", "")
            return redirect("input_message")
        return render(request, "marquee/input_message.html", {"message": GLOBAL_MESSAGE})
    else:
        return redirect('/login')

def get_message_json(request):
    return JsonResponse({"message": GLOBAL_MESSAGE})