from django.urls import path, include
from . import chatbot,views

urlpatterns = [
    path('chatbot', chatbot.request_to_chatbot),
    path('', views.test)
]
