from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .views.general_chatbot import general_chatbot
from .views.word_chatbot import word_chatbot
@csrf_exempt
def request_to_chatbot(request):  # chatbot 요청을 처리하는 함수
    if request.method == "POST":
        prompt = str(request.POST.get("message"))
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