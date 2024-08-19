from django.urls import path
from . import view,login

urlpatterns = [
    path('chatbot', view.request_to_chatbot, name='chatbot'),
    path('sentence', view.request_to_sentence, name='sentence'),
    path('save',view.save, name='save'),
    path('login', login.login_view, name='login'),
]

