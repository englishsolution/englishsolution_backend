from django.urls import path, include
from . import chatbot,views

urlpatterns = [
    # path('chatbot', views.query_view_chatbot)
    path('chatbot', chatbot.chatbot),
    path('', views.test)
]
