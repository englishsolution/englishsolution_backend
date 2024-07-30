"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app_video import views, speaking, scripts, quiz

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', scripts.test, name='test'),
    path('insert_url/', scripts.insert_url, name='insert_url'),
    path('processing_url/', scripts.processing_url, name='processing_url'),
    path('speaking/', speaking.speaking, name='speaking'),
    path('processing_speaking/', speaking.processing_speaking, name='processing_speaking'),
    path('select_quiz/', quiz.select_quiz, name='select_quiz'),
    path('all_sentence_quiz/', quiz.all_sentence_quiz, name='all_sentence_quiz'),
    path('all_word_quiz/', quiz.all_word_quiz, name='all_word_quiz'),
    path('replay_word_quiz/', quiz.replay_word_quiz, name='replay_word_quiz'),
    path('replay_sentence_quiz/', quiz.replay_sentence_quiz, name='replay_sentence_quiz'),
]
