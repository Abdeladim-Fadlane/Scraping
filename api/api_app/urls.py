from django.contrib import admin
from .views import TaskListCreateAPIView, TaskRetrieveUpdateDestroyAPIView
from django.urls import path, include


urlpatterns = [
    path('tasks/', TaskListCreateAPIView.as_view() ,name='task-list-create'),
    path('tasks/<int:pk>/', TaskRetrieveUpdateDestroyAPIView.as_view() ,name='task-retrieve-update-destroy'),
]