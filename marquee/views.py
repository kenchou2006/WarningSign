from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import GlobalMessage

GLOBAL_MESSAGE = ""

def load_message_from_db():
    global GLOBAL_MESSAGE
    try:
        msg = GlobalMessage.objects.latest('updated_at')
        GLOBAL_MESSAGE = msg.content
    except GlobalMessage.DoesNotExist:
        GLOBAL_MESSAGE = ""

def input_message(request):
    global GLOBAL_MESSAGE
    if request.user.is_authenticated:
        if request.method == "POST":
            GLOBAL_MESSAGE = request.POST.get("message", "")
            GlobalMessage.objects.create(content=GLOBAL_MESSAGE)
            return redirect("input_message")
        if not GLOBAL_MESSAGE:
            load_message_from_db()
        return render(request, "marquee/input_message.html", {"message": GLOBAL_MESSAGE})
    else:
        return redirect('/login')

def get_message_json(request):
    global GLOBAL_MESSAGE
    if not GLOBAL_MESSAGE:
        load_message_from_db()
    response = JsonResponse({"message": GLOBAL_MESSAGE})
    response["Access-Control-Allow-Origin"] = "*"
    return response