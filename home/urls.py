from django.contrib import admin
from django.urls import path
from home import views


# urlpatterns = [
#     path('', views.index, name='home'),
#     path('result/', views.result, name='result'),  
#     path('result/production', views.production, name='production'),
#     path('userdetails/', views.user_details, name='userdetails')
#     # path('result/pricing', views.pricing, name='pricing')        
# ]

urlpatterns = [
    path('', views.userdetail, name='userdetail'),
    path('solarcalculator', views.index, name='index'),
    path('result/', views.result, name='result'),
    path('result/production/', views.production, name='production'),
    path('result/production/report/', views.report, name='report')     
]