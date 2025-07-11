from django.urls import path
from . import views

urlpatterns = [
    path('marquee/input/', views.input_message, name="input_message"),
    path('marquee/message_json/', views.get_message_json, name="message_json"),
    path('marquee/settings/', views.auto_message_settings, name="auto_message_settings"),
    path('marquee/auto_on/', views.auto_message_on, name="auto_message_on"),
    path('marquee/auto_off/', views.auto_message_off, name="auto_message_off"),
]