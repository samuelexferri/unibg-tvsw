from django.urls import path, include
from rest_framework import routers

from timetable import views

app_name = 'timetable'

router = routers.DefaultRouter()
router.register(r'timetable/api', views.TimetableViewSet, basename='timetableapi')

urlpatterns = [
    path('', views.homepage, name='home'),
    path(r'', include(router.urls)),
    path('timetable/', views.view, name='view_timetable'),
    path('timetable/calc', views.calculate, name='calc_timetable'),
]
