from django.urls import path,include
from . import view,login
from rest_framework.routers import DefaultRouter
from .view import SentenceViewSet,WordViewSet

router = DefaultRouter()
router.register(r'sentences', SentenceViewSet)
router.register(r'words',WordViewSet)

urlpatterns = [
    path('chatbot', view.request_to_chatbot, name='chatbot'),
    path('sentence', view.request_to_sentence, name='sentence'),
    path('save',view.save, name='save'),
    path('login', login.login_view, name='login'),
    path('realtime/', include(router.urls)),
]

