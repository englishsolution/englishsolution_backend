import json
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
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
                   f"        \"word_korean1\","
                   f"        \"word_korean2\","
                   f"        \"word_korean3\","
                   f"        \"word_korean4\""
                   f"      ],"
                   f"      \"answer\": \"word_korean2\""
                   f"    }},"
                   f"}},"
                   f"Answer each word with JSON in the form of an example. The number of words and the number of questions should be the same")

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

@csrf_exempt
def quiz_index(request):
    data = json.loads(request.body.decode('utf-8'))
    if request.method == 'POST':
        user_id=data.get("user_id")
        titles = Video.objects.filter(user_id=user_id).values_list('title', flat=True)
        titles= list(titles)
        return JsonResponse({'titles': titles})
    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def all_sentence_quiz(request):
    data = json.loads(request.body.decode('utf-8'))
    if request.method == 'POST':
        user_id=data.get("user_id")
        video_id=data.get("video_id")
        sentences=''
        #문장이 없는 경우
        count=Sentence.objects.count()
        if(count==0):
            return JsonResponse({'error': '저장된 문장이 없음'}, status=400)
        elif (count<=10):
            sentence_list=Sentence.objects.filter(video_id=video_id).values_list('sentence_eg', flat=False)
            sentences = " / ".join([sentence[0] for sentence in sentence_list])
        elif (count>10):
            random_sentence_list = Sentence.objects.filter(video_id=video_id).order_by(Random()).values_list('sentence_eg', flat=True)[:10]
            sentences = " / ".join(random_sentence_list)

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
        json_quiz = json.loads(response_text)

        #마지막 quiz_id
        last_quiz_id = Quiz.objects.order_by('-video_id').values_list('video_id', flat=True).first()
        if(last_quiz_id==None):
            last_quiz_id=0
        #quiz, sentence_quiz 테이블에 저장
        new_quiz = Quiz(
            quiz_date=timezone.now(),
            answer_per=0,
            user_id=user_id,
            video_id=video_id,
        )
        new_quiz.save()

        #인스턴스 가져오기
        quiz_instance = Quiz.objects.get(quiz_id=last_quiz_id+1)
        questions = json_quiz.get("questions", [])
        quiz_id_list =[]
        # 각 질문 데이터 그대로 가져오기
        for question in questions:
            sentence_quiz = SentenceQuiz(
                quiz=question,
                is_wrong=1,
                quiz_0=quiz_instance
            )
            sentence_quiz.save()
            latest_quiz_id = SentenceQuiz.objects.latest('sentence_quiz_id').sentence_quiz_id
            quiz_id_list.append(latest_quiz_id)
        return JsonResponse({'json_quiz': json_quiz,
                             'quiz_id_list': quiz_id_list})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def all_word_quiz(request):
    data = json.loads(request.body.decode('utf-8'))
    if request.method == 'POST':
        user_id = data.get("user_id")
        video_id = data.get("video_id")
        words=''
        # 문장이 없는 경우
        count = Word.objects.count()
        if (count == 0):
            return JsonResponse({'error': '저장된 문장이 없음'}, status=400)
        elif (count <= 10):
            word_list = Word.objects.filter(video_id=video_id).values_list('word_eg', flat=False)
            words = " / ".join(word[0] for word in word_list)
        elif (count > 10):
            random_word_list = Word.objects.filter(video_id=video_id).order_by(Random()).values_list('word_eg', flat=True)[:10]
            words = " / ".join(random_word_list)

        # ChatGPT 모델 호출 및 응답 받기
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f'words : {words} \n'+request_content_word}
            ],
            max_tokens=2000,
            temperature=0.8,
            # response_format 지정하기
            response_format={"type": "json_object"}
        )

        response_text = response.choices[0].message.content
        json_quiz = json.loads(response_text)

        # 마지막 quiz_id
        last_quiz_id = Quiz.objects.order_by('-video_id').values_list('video_id', flat=True).first()
        if (last_quiz_id == None):
            last_quiz_id = 0
        # quiz, sentence_quiz 테이블에 저장
        new_quiz = Quiz(
            quiz_date=timezone.now(),
            answer_per=0,
            user_id=user_id,
            video_id=video_id,
        )
        new_quiz.save()
        # 인스턴스 가져오기
        quiz_instance = Quiz.objects.get(quiz_id=last_quiz_id + 1)
        questions = json_quiz.get("questions", [])
        quiz_id_list = []
        # 각 질문 데이터 그대로 가져오기
        for question in questions:
            word_quiz = WordQuiz(
                quiz=question,
                is_wrong=1,
                quiz_0=quiz_instance
            )
            word_quiz.save()
            latest_quiz_id = WordQuiz.objects.latest('word_quiz_id').word_quiz_id
            quiz_id_list.append(latest_quiz_id)
        return JsonResponse({'json_quiz': json_quiz,
                             'quiz_id_list': quiz_id_list})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def replay_quiz(request):
    data = json.loads(request.body.decode('utf-8'))
    if request.method == 'POST':
        user_id = data.get("user_id")
        video_id = data.get("video_id")

        quiz_ids = Quiz.objects.filter(user=user_id, video=video_id).values_list('quiz_id', flat=True)
        sentence_quiz = SentenceQuiz.objects.filter(quiz_0__in=quiz_ids, is_wrong=1).values('quiz','sentence_quiz_id')
        word_quiz = WordQuiz.objects.filter(quiz_0__in=quiz_ids, is_wrong=1).values('quiz','word_quiz_id')

        sentence_count = sentence_quiz.count()
        word_count = word_quiz.count()
 
        if(sentence_count==0 & word_count == 0 ):
            return JsonResponse({'error': '틀린 문장과 단어가 없음'}, status=400)
        
        if (sentence_count>5) :
            print('>5')
            sentence_quiz=sentence_quiz.order_by('?')[:5].values_list('quiz','sentence_quiz_id')
            
        if (word_count > 5):
            print('>5')
            word_quiz = word_quiz.order_by('?')[:5].values_list('quiz','word_quiz_id')

        json_sentence_quiz = list(sentence_quiz)
        json_word_quiz = list(word_quiz)

        return JsonResponse({
            'word_quiz': json_word_quiz,
            'sentence_quiz': json_sentence_quiz
        }, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=400)