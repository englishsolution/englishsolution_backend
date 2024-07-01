from django.shortcuts import render
from django.http import JsonResponse
from .models import Test
from dotenv import load_dotenv
import os
import openai

load_dotenv(verbose=True) #env 파일에서 api_key를 가져옴

openai.api_key = os.getenv("OPENAI_API_KEY") #openai api key 연결

def chatbot(request):
    print(request) # to check
    query = openai.ChatCompletion.create(
        models="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": request}
        ],
        max_tokens=1024, # chat 에서 생성해낼 수 있는 최대 tokens 수
        stop=None, # 대화의 종류를 명시, None -> 종료 조건 x
        temperature=0.5, #0~2사이의 값, 높을 수록 더 랜덤한 response 발생, 낮을 수록 보다 정확한 정보 제공
    )
    response = query.choices[0].messages["content"]
    print(response)
    return response

def query_view_chatbot(request):
    if request.method == "POST":
        prompt = str(request.POST["prompt"])
        response = chatbot(prompt)
        return JsonResponse({'response':response})
    return render(request, "app_video/chatbot.html")


# Create your views here.
def test(request):
    tests = Test.objects.all()
    return render(request, 'app_video/index.html', {"tests":tests})
