from django.utils import timezone
from django.http import JsonResponse, request, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .form import SentenceForm,WordForm
from .views.general_chatbot import general_chatbot
from .views.word_chatbot import word_chatbot
from .views.sentence_analysis import sentence_analysis

@csrf_exempt
def request_to_chatbot(request):  # chatbot 요청을 처리하는 함수
    if request.method == "POST":
        prompt = str(request.POST.get("prompt"))
        mode= str(request.POST.get("mode"))
        if mode == "general": #일반 chatbot
            response = general_chatbot(prompt)
        #elif mode=="conversation": # 영상의 주제를 가지고 대화하는 챗봇
         #   response = conversation_chatbot(prompt)
        elif mode == "word":  # 랜덤 단어를 제공해주는 챗봇
            diffculty = str(request.POST.get("diffculty"))
            response = word_chatbot(diffculty)
        return JsonResponse({'reply': response})
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
