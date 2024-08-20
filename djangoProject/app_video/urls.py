from django.urls import path,include
from . import view,login
from rest_framework.routers import DefaultRouter
from .view import SentenceViewSet,WordViewSet
from app_video import view, speaking, scripts, quiz, tests, user

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

    path('processing_url/', scripts.processing_url, name='processing_url'),
    path('speaking/', speaking.speaking, name='speaking'),
    path('processing_speaking/', speaking.processing_speaking, name='processing_speaking'),
    path('all_sentence_quiz/', quiz.all_sentence_quiz, name='all_sentence_quiz'),
    path('all_word_quiz/', quiz.all_word_quiz, name='all_word_quiz'),
    path('replay_word_quiz/', quiz.replay_word_quiz, name='replay_word_quiz'),
    path('replay_sentence_quiz/', quiz.replay_sentence_quiz, name='replay_sentence_quiz'),
    path('request_to_chatbot/', tests.request_to_chatbot, name='request_to_chatbot'),
    path('signup/', user.signup, name='signup'),
    path('activate/<uidb64>/<token>/', user.activate, name='activate'),
    path('check_id/', user.check_id, name='check_id'),
    path('logout/', user.logout, name='logout'),
    path('login/', user.login, name='login'),
    path('delete/', user.delete, name='delete'),
