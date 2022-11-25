from django.contrib import admin
from django.urls import path
from rest_framework import routers
from django.urls import include
from .views import AlarmViewSet, ScadaPointViewSet


router = routers.DefaultRouter()
router.register('alarms', AlarmViewSet)
router.register('points', ScadaPointViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
