from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import MarqueeMessage,SignOnMessage,SignOffMessage,MarqueeSettings
from app.views import get_waringsign_status

DISPLAY_MESSAGE = ""
AUTO_MESSAGE = False
SIGNON_MESSAGE = ""
SIGNOFF_MESSAGE = ""
SIGN_MODE=False

def load_message_from_db():
    global DISPLAY_MESSAGE, SIGNON_MESSAGE, SIGNOFF_MESSAGE, AUTO_MESSAGE
    try:
        msg = MarqueeMessage.objects.latest('updated_at')
        DISPLAY_MESSAGE = msg.content
    except MarqueeMessage.DoesNotExist:
        DISPLAY_MESSAGE = ""
    try:
        signon = SignOnMessage.objects.latest('updated_at')
        SIGNON_MESSAGE = signon.content
    except SignOnMessage.DoesNotExist:
        SIGNON_MESSAGE = ""
    try:
        signoff = SignOffMessage.objects.latest('updated_at')
        SIGNOFF_MESSAGE = signoff.content
    except SignOffMessage.DoesNotExist:
        SIGNOFF_MESSAGE = ""
    try:
        settings = MarqueeSettings.objects.latest('updated_at')
        AUTO_MESSAGE = settings.auto_message
    except MarqueeSettings.DoesNotExist:
        AUTO_MESSAGE = False

def auto_message_on(request):
    global AUTO_MESSAGE
    AUTO_MESSAGE = True
    MarqueeSettings.objects.create(auto_message=True)
    return redirect('auto_message_settings')

def auto_message_off(request):
    global AUTO_MESSAGE
    AUTO_MESSAGE = False
    MarqueeSettings.objects.create(auto_message=False)
    return redirect('auto_message_settings')

def auto_message_settings(request):
    global AUTO_MESSAGE, SIGNON_MESSAGE, SIGNOFF_MESSAGE
    auto_message = AUTO_MESSAGE
    signon = SignOnMessage.objects.latest('updated_at') if SignOnMessage.objects.exists() else None
    signoff = SignOffMessage.objects.latest('updated_at') if SignOffMessage.objects.exists() else None
    if request.method == "POST" and auto_message:
        if 'signon_content' in request.POST:
            SignOnMessage.objects.create(content=request.POST['signon_content'])
            SIGNON_MESSAGE = request.POST['signon_content']
        if 'signoff_content' in request.POST:
            SignOffMessage.objects.create(content=request.POST['signoff_content'])
            SIGNOFF_MESSAGE = request.POST['signoff_content']
        return redirect('auto_message_settings')
    return render(request, "marquee/settings.html", {
        "auto_message": auto_message,
        "signon": signon,
        "signoff": signoff
    })

def input_message(request):
    global DISPLAY_MESSAGE
    if request.user.is_authenticated:
        if request.method == "POST":
            DISPLAY_MESSAGE = request.POST.get("message", "")
            MarqueeMessage.objects.create(content=DISPLAY_MESSAGE)
            return redirect("input_message")
        if not DISPLAY_MESSAGE:
            load_message_from_db()
        return render(request, "marquee/input_message.html", {"message": DISPLAY_MESSAGE})
    else:
        return redirect('/login')

def get_message_json(request):
    global DISPLAY_MESSAGE, AUTO_MESSAGE, SIGNON_MESSAGE, SIGNOFF_MESSAGE, SIGN_MODE
    if not DISPLAY_MESSAGE:
        load_message_from_db()
    if not AUTO_MESSAGE:
        response = JsonResponse({"message": DISPLAY_MESSAGE})
    else:
        waringsign_status = get_waringsign_status()
        if waringsign_status == 1:
            response = JsonResponse({"message": SIGNON_MESSAGE})
        elif waringsign_status == 2:
            response = JsonResponse({"message": SIGNOFF_MESSAGE})
        else:
            response = JsonResponse({"message": DISPLAY_MESSAGE})
    response["Access-Control-Allow-Origin"] = "*"
    return response