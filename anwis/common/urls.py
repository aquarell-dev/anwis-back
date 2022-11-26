from django.urls import path

from common.views import TaskListCreateView

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view()),
]
