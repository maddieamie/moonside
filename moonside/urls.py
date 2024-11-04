from django.urls import path, include

from moonside import views

urlpatterns = [
    path('', views.home, name='moonside'),
]