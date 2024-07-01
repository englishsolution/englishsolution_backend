from django.urls import path, include
from . import views

urlpatterns = [
    # path('chatbot', views.query_view_chatbot)
    path('chatbot',views.chatbot)
]
