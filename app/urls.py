from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('cleancache/',views.cleanCache),
    #Sign1
    path('sign1/',views.Sign1),
    path('input/', views.input_page),
    path('output/', views.output_page),
    path('input/off/', views.input_off_page),
    path('output/off/', views.output_off_page),
    path('arduino_info/',views.arduino_info),
    #Sign2
    path('sign2/',views.Sign2),
    path('input2/', views.input_page2),
    path('output2/', views.output_page2),
    path('input2/off/', views.input_off_page2),
    path('output2/off/', views.output_off_page2),
    path('arduino_info2/',views.arduino_info2),
    #ServerView
    #path('serverinfo/',views.server_info),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('access-records/', views.access_record_list, name='access_record_list'),
    path('clear-access-records/', views.clear_access_records, name='clear_access_records'),
]