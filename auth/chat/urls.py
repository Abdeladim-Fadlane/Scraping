from django.urls import path
from . import views

urlpatterns = [
    path('room/', views.ft),
    # path('join_game/', views.join_game,name='join_game'),
]