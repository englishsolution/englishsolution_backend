import json
from datetime import datetime

from django.shortcuts import render
from dotenv import load_dotenv
from openai import OpenAI
import os

from app_video.models import Video, Sentence, Word, Quiz, SentenceQuiz, WordQuiz
from django.db.models.functions import Random

load_dotenv(verbose=True) #env 파일에서 api_key를 가져옴 # 배포시 verbose 지우기

API_KEY=os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=API_KEY)

request_content_word = (f"Purpose: Choose the correct korean of a word. "
                   f"example:\n"
                   f"{{"
                   f"  \"questions\": ["
                   f"    {{"
                   f"      \"word\": \"word_english\","
                   f"      \"options\": ["
                   f"        \"A. word_korean1\","
                   f"        \"B. word_korean2\","
                   f"        \"C. word_korean3\","
                   f"        \"D. word_korean4\""
                   f"      ],"
                   f"      \"answer\": \"word_korean2\""
                   f"    }},"
                   f"}},"
                   f"Answer each word with JSON in the form of an example. Make the total number of words")

request_content_sentence = (f"Purpose: Fill in the blanks. "
                        f"example:\n"
                        f"{{"
                        f"  \"questions\": ["
                        f"    {{"
                        f"      \"sentence\": \"But I told you to get each one of them an ice cream why did you buy all that bread honey cut me some slack _ ya.\","
                        f"      \"options\": ["
                        f"        \"will\","
                        f"        \"should\","
                        f"        \"would\","
                        f"        \"can\""
                        f"      ],"
                        f"      \"answer\": \"can\""
                        f"    }},"
                        f"}}"
                        f"For each sentence, fill in a blank space with an important word or vocabulary and change it to \'_\'."
                        f" Return JSON in the same format as in the example")

def select_quiz(request):
    videos = Video.objects.all()
    return render(request, 'app_video/select_quiz.html', {"videos": videos})

def all_sentence_quiz(request):
    if request.method == 'POST':
        video_id=1
        sentences=''
        #문장이 없는 경우
        count=Sentence.objects.count()
        if(count==0):
            print('문장 없음~~')
            return render(request, 'app_video/select_quiz.html', {
            })
        elif (count<=10):
            print('<=10')
            sentence_list=Sentence.objects.filter(video_id=video_id).values_list('sentence_eg', flat=False)
            sentences= " / ".join(sentence_list)
            print(sentences)
        elif (count>10):
            print('>10')
            random_sentence_list = Sentence.objects.filter(video_id=video_id).order_by(Random()).values_list('sentence_eg', flat=True)[:10]
            sentences = " / ".join(random_sentence_list)
            print(sentences)

        # ChatGPT 모델 호출 및 응답 받기
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f'sentences: {sentences}'+ request_content_sentence}
            ],
            max_tokens=1000,
            temperature=0.8,
            # response_format 지정하기
            response_format = {"type": "json_object"}
        )

        response_text = response.choices[0].message.content
        print(response_text)
        json_quiz = json.loads(response_text)

        #마지막 quiz_id
        last_quiz_id = Quiz.objects.order_by('-video_id').values_list('video_id', flat=True).first()
        if(last_quiz_id==None):
            last_quiz_id=0
        # quiz, sentence_quiz 테이블에 저장
        new_quiz = Quiz(
            user_id='user1',
            video_id=video_id,
            quiz_date=datetime.now(),
        )
        new_quiz.save()
        #인스턴스 가져오기
        quiz_instance = Quiz.objects.get(quiz_id=last_quiz_id+1)

        for quiz_data in json_quiz.values():
            sentence_quiz = SentenceQuiz(
                quiz_id=quiz_instance,
                quiz=quiz_data,
                is_wrong=1
            )
            sentence_quiz.save()


        return render(request, 'app_video/select_quiz.html', {
                "json_quiz": json_quiz
        })

def all_word_quiz(request):
    if request.method == 'POST':
        video_id=1
        words=''
        # 문장이 없는 경우
        count = Word.objects.count()
        if (count == 0):
            print('단어 없음~~')
            return render(request, 'app_video/select_quiz.html', {
            })
        elif (count <= 10):
            print('<=10')
            word_list = Word.objects.filter(video_id=video_id).values_list('word_eg', flat=False)
            words = " / ".join(word_list)
            print(words)
        elif (count > 10):
            print('>10')
            random_word_list = Word.objects.filter(video_id=video_id).order_by(Random()).values_list('word_eg', flat=True)[:10]
            words = " / ".join(random_word_list)
            print(words)

        # ChatGPT 모델 호출 및 응답 받기
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f'words : {words}'+request_content_word}
            ],
            max_tokens=2000,
            temperature=0.8,
            # response_format 지정하기
            response_format={"type": "json_object"}
        )

        response_text = response.choices[0].message.content
        print(response_text)
        json_quiz = json.loads(response_text)

        # 마지막 quiz_id
        last_quiz_id = Quiz.objects.order_by('-video_id').values_list('video_id', flat=True).first()
        if (last_quiz_id == None):
            last_quiz_id = 0
        # quiz, sentence_quiz 테이블에 저장
        new_quiz = Quiz(
            user_id='user1',
            video_id=video_id,
            quiz_date=datetime.now(),
        )
        new_quiz.save()
        # 인스턴스 가져오기
        quiz_instance = Quiz.objects.get(quiz_id=last_quiz_id + 1)

        for quiz_data in json_quiz.values():
            word_quiz = WordQuiz(
                quiz_id=quiz_instance,
                quiz=quiz_data,
                is_wrong=1
            )
            word_quiz.save()

        return render(request, 'app_video/select_quiz.html', {
            "json_quiz": json_quiz
        })

def replay_sentence_quiz(request):
    if request.method == 'POST':
        video_id=1
        sentences=''
        #문장이 없는 경우
        count=SentenceQuiz.objects.filter(is_wrong=1, video_id = video_id).count()
        if(count==0):
            print('문장 없음~~')
            return render(request, 'app_video/select_quiz.html', {
            })
        elif (count<=10):
            print('<=10')
            json_quiz=SentenceQuiz.objects.filter(video_id=1, is_wrong=1).values_list('quiz', flat=True)
        elif (count>10):
            print('>10')
            json_quiz = SentenceQuiz.objects.filter(video_id=1, is_wrong=1).order_by('?')[:10].values_list('quiz', flat=True)

        return render(request, 'app_video/select_quiz.html', {
                "json_quiz": json_quiz
        })

def replay_word_quiz(request):
    if request.method == 'POST':
        video_id=1
        words=''
        # 문장이 없는 경우
        count = WordQuiz.objects.filter(is_wrong=1, video_id = video_id).count()
        if (count == 0):
            print('단어 없음~~')
            return render(request, 'app_video/select_quiz.html', {
            })
        elif (count <= 10):
            print('<=10')
            json_quiz = WordQuiz.objects.filter(video_id=1, is_wrong=1).values_list('quiz', flat=True)
        elif (count > 10):
            print('>10')
            json_quiz = WordQuiz.objects.filter(video_id=1, is_wrong=1).order_by('?')[:10].values_list('quiz',flat=True)

        return render(request, 'app_video/select_quiz.html', {
            "json_quiz": json_quiz
        })