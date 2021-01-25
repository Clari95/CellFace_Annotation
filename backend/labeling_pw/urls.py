from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('getDataLevel/<str:user>/<str:tooltype>/<str:dataset_typ>/<int:level_num>', views.getDataLevel),
    path('labelmask/', views.getData, name='label_mask'),
    path('getData/<int:number>/<str:mounted>/<str:user>/<int:image_section>/<str:dataset_typ>/<str:tooltype>/<int:level_num>', views.getData, name='label_mask'),
    #path('label/', views.labels_received, name='label_received'),
    path('label_level/<str:data>/<str:data_region>/<str:lastEle>/<int:number>/<str:user>/<str:dataset_typ>/<int:level_num>/<str:tooltype>', views.labels_received_level, name='label_received'),
    path('label/<str:data>/<str:data_region>/<str:lastEle>/<int:number>/<str:user>/<str:dataset_typ>/<int:level_num>/<str:tooltype>', views.labels_received, name='label_received'),
    path('newAreas/', views.new_areas, name='new_areas'),
    path('newAreas/<str:data>/<int:number>/<str:user>/<str:dataset_typ>/<int:level_num>', views.new_areas, name='new_areas'),
    path('getDataReview/<str:user>/<str:dataset_typ>/<str:tooltype>/<int:numberImages>', views.getDataReview, name='getSegMask'),
    path('updateScore/<str:tooltype>/<str:user>/<str:dataset_typ>/<str:allScores>/<str:date>', views.updateScores),
    path('updateScoreGame/<str:tooltype>/<str:user>/<str:dataset_typ>/<str:allScores>/<str:date>', views.updateScoresGame),
    path('getAccuracy/<str:tooltype>/<str:user>/<str:dataset_typ>/<int:level_num>/<int:numberImages>', views.getAccuracy),
    path('getAccuracy_level/<int:level_num>/<int:numberImages>/<str:acc_allImages>', views.getAccuracy_level),
]
