from django.urls import path

from transfer import views

app_name = 'transfer'

urlpatterns = [
    path('', views.homepage, name='home'),
    path('transfer/', views.transfer, name='transfer'),
]
