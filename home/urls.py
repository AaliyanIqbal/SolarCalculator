from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('', views.index, name='home'),
    path('result/', views.result, name='result'),  
    path('result/production', views.production, name='production'),
    path('result/pricing', views.pricing, name='pricing')        
]