from django.utils import timezone
from django.http import JsonResponse, request, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .views.general_chatbot import general_chatbot
from .views.word_chatbot import word_chatbot
from .views.conversation_chatbot import conversation_chatbot
from .views.sentence_analysis import sentence_analysis
from .views.word_translate import word_translate
from .views.sentence_translate import sentence_translate
import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Word,Sentence,Video
from .serializers import SentenceSerializer,WordSerializer ,VideoSerializer
from rest_framework import viewsets

class SentenceViewSet(viewsets.ModelViewSet):
    queryset = Sentence.objects.all()
    serializer_class = SentenceSerializer

class WordViewSet(viewsets.ModelViewSet):
    queryset = Word.objects.all()
    serializer_class = WordSerializer

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

  #  def get_queryset(self):
  #      user = self.request.user
  #      return Video.objects.filter(user=user)

@login_required
def dashboard(request):
    return render(request, 'app_video/dashboard.html')

@csrf_exempt
def testserver(request):
    return HttpResponse("server is running!")

@csrf_exempt
def request_to_chatbot(request):  # chatbot 요청을 처리하는 함수
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))
            mode = data.get("mode")
            print("mode:",mode)  #서버 확인용
            check = 0

            if mode == "general":  # 일반 chatbot
                prompt = data.get("prompt")
                print("prompt:",prompt) #서버 확인용
                response = general_chatbot(prompt)
                check = 1
            elif mode == "word":  # 랜덤 단어를 제공해주는 챗봇
                difficulty = data.get("difficulty")
                print("difficulty:",difficulty) #서버 확인용
                response = word_chatbot(difficulty)
                check = 1
            elif mode =="topic": # 영상 주제를 가지고 영어로 대화하는 챗봇
                prompt = data.get("prompt")
                print("prompt:",prompt) #서버 확인용
                video_title = data.get("video_title")
                response = conversation_chatbot(prompt,video_title)
                check=1
            else:
                raise ValueError(f"Invalid mode: {mode}")

            print("response:",response) #서버 확인용

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
        data = json.loads(request.body.decode('utf-8'))
        sentence = data.get("sentence")
        print("sentence:",sentence) #서버 확인용
        response = sentence_analysis(sentence)
        print("response:",response) #서버 확인용
    return JsonResponse({'reply': response})

@csrf_exempt
def save(request): # 사용자가 저장한 것을 데이터베이스에 연결하는 함수
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        category = data.get("category") #word or sentence
        print("category:",category) #서버 확인용

        if category == "word" :
           word=data.get("word")
           find_video_link=data.get("video_link")
           word_eg,word_kr,type=word_translate(word)
           print("word_eg:",word_eg,"word_kr:",word_kr,"type:",type) #서버 확인용

           # Video 인스턴스 가져오기
           try:
               video_link = Video.objects.get(link=find_video_link)
           except Video.DoesNotExist:
               return JsonResponse({'error': 'Invalid video ID'}, status=400)

           save_word = Word(word_eg=word_eg, word_kr=word_kr, video=video_link,type=type)
           save_word.save()
           return JsonResponse({'message': 'Word saved successfully'}, status=201)


        elif category == 'sentence':
            sentence = data.get("sentence")
            find_video_link = data.get("video_link")
            korean=sentence_translate(sentence)

            # Video 인스턴스 가져오기
            try:
                video_link = Video.objects.get(link=find_video_link)
            except Video.DoesNotExist:
                return JsonResponse({'error': 'Invalid video ID'}, status=400)

            save_sentence = Sentence(sentence_eg=sentence,sentence_kr=korean,video=video_link)
            save_sentence.save()
            return JsonResponse({'message': 'sentence saved successfully'}, status=201)
