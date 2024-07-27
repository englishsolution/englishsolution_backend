from django.urls import path
from . import view

urlpatterns = [
    path('chatbot', view.request_to_chatbot, name='chatbot'),
    path('sentence', view.request_to_sentence, name='sentence'),

]
