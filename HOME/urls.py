from django import urls
from django.urls import path
from . import views

urlpatterns = [
    path('',views.krlang),
    path('krlang/',views.clear_list_KR),
    path('vnlang/',views.clear_list_VN),
    path('result_KR/',views.CHOICES_KR, name='result_KR'),
    path('result_VN/',views.CHOICES_VN, name='result_VN')
]