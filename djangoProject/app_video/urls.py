from django.urls import path,include
# from app_video import view, speaking, scripts, quiz, tests, user

from . import view,login, speaking, scripts, quiz, tests, user
from rest_framework.routers import DefaultRouter
from .view import SentenceViewSet, WordViewSet, VideoViewSet

router = DefaultRouter()
router.register(r'sentences', SentenceViewSet)
router.register(r'words',WordViewSet)
router.register(r'videos',VideoViewSet)

from django.contrib import admin
from django.urls import path
# from app_video import view, speaking, scripts, quiz, tests, user

urlpatterns = [
    path('testserver',view.testserver),
    path('chatbot', view.request_to_chatbot, name='chatbot'),
    path('sentence', view.request_to_sentence, name='sentence'),
    path('save',view.save, name='save'),
    path('login', login.login_view, name='login'),
    path('realtime/', include(router.urls)),

    path('processing_url/', scripts.processing_url, name='processing_url'),
    path('speaking/', speaking.speaking, name='speaking'),
    path('processing_speaking/', speaking.processing_speaking, name='processing_speaking'),
    path('all_sentence_quiz/', quiz.all_sentence_quiz, name='all_sentence_quiz'),
    path('all_word_quiz/', quiz.all_word_quiz, name='all_word_quiz'),
    path('replay_quiz/', quiz.replay_quiz, name='replay_quiz'),
    path('request_to_chatbot/', tests.request_to_chatbot, name='request_to_chatbot'),
    path('signup/', user.signup, name='signup'),
    path('activate/<uidb64>/<token>/', user.activate, name='activate'),
    path('check_id/', user.check_id, name='check_id'),
    path('logout/', user.logout, name='logout'),
    path('login/', user.login, name='login'),
    path('delete/', user.delete, name='delete'),

    path('quiz_index/', quiz.quiz_index, name='quiz_index'),
    path('quiz_result/', quiz.quiz_result, name='quiz_result'),

]