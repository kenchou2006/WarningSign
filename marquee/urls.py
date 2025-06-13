from django.urls import path
from . import views

urlpatterns = [
    path('marquee/input/', views.input_message, name="input_message"),
    path('marquee/message_json/', views.get_message_json, name="message_json"),
]