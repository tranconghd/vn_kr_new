from django import urls
from django.urls import path
from . import views

urlpatterns = [
    path('krlang/',views.krlang, name='krlang'),
    path('',views.krlang, name='krlang'),
    path('vnlang/',views.vnlang, name='vnlang'),
    path('krlang/result_KR/',views.result_KR, name='result_KR'),
    path('vnlang/result_VN/',views.result_VN, name='result_VN')
    
]