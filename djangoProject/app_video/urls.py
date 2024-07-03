from django.urls import path, include
from . import chatbot

urlpatterns = [
    # path('chatbot', views.query_view_chatbot)
    path('chatbot',chatbot.chatbot)
]
