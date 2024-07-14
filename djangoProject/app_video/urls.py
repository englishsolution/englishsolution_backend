from django.urls import path, include
from . import chatbot,views

urlpatterns = [
    path('', chatbot.request_to_chatbot, name='chatbot'),
    path('test',views.test)
]
