from django.utils import timezone
from django.http import JsonResponse, request, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .form import SentenceForm,WordForm
from .views.general_chatbot import general_chatbot
from .views.word_chatbot import word_chatbot
from .views.conversation_chatbot import conversation_chatbot
from .views.sentence_analysis import sentence_analysis
import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, 'app_video/dashboard.html')

@csrf_exempt
def request_to_chatbot(request):  # chatbot 요청을 처리하는 함수
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))
            mode = data.get("mode")

            check = 0

            if mode == "general":  # 일반 chatbot
                prompt = data.get("prompt")
                response = general_chatbot(prompt)
                check = 1
            elif mode == "word":  # 랜덤 단어를 제공해주는 챗봇
                difficulty = data.get("difficulty")
                response = word_chatbot(difficulty)
                check = 1
            elif mode =="topic": # 영상 주제를 가지고 영어로 대화하는 챗봇
                prompt = data.get("prompt")
                video_title = data.get("video_title")
                response = conversation_chatbot(prompt,video_title)
                check=1
            else:
                raise ValueError(f"Invalid mode: {mode}")

            if check == 1:
                return JsonResponse({'reply': response}, status=200)
            else:
                return JsonResponse({'error': 'No valid response generated'}, status=500)
        except ValueError as ve:
            # 예외: 잘못된 입력값
            return JsonResponse({'error': str(ve)}, status=400)
        except Exception as e:
            # 일반 예외 처리
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def request_to_sentence(request): # 문장 분석을 하는 함수
    if request.method == "POST":
        sentence = str(request.POST.get("sentence"))
        response = sentence_analysis(sentence)
    return JsonResponse({'reply': response})

@csrf_exempt
def save(request): # 사용자가 저장한 것을 데이터베이스에 연결하는 함수
    if request.method == 'POST':
        category = str(request.POST.get("category"))

        if category == "sentence" :
            form = SentenceForm(request.POST)
            if form.is_valid():
                sentence = form.save(commit=False) #commit = False는 당장 저장 x -> 특정 행위 후 저장
                sentence.save_date=timezone.now()
                sentence.save()
                return HttpResponse('success')  # 저장 성공
            else:
                return HttpResponse('form invalid', status=400)  # 폼 유효성 검사 실패

        elif category == 'word':
            form = WordForm(request.POST)
            if form.is_valid():
                word = form.save(commit=False)
                word.save_date = timezone.now()
                word.save()
                return HttpResponse('success')  # 저장 성공
            else:
                return HttpResponse('form invalid', status=400)  # 폼 유효성 검사 실패

        return HttpResponse('false', status=400)  # 잘못된 요청
