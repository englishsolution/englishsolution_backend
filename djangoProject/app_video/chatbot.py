from django.shortcuts import render
from django.http import JsonResponse
from dotenv import load_dotenv
from openai import OpenAI
import os
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

load_dotenv(verbose=True) #env 파일에서 api_key를 가져옴 ######## 배포시 verbose 지우기
API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY)

message_history=[]

#chatbot을 열면 실행되는 메소드
def chatbot(prompt, message_history=[]):
    #prompt=input("prompt 입력:")

    if prompt == "exit":
        return "Exiting", message_history

    message_history.append(  # to consecutive message
        {
            "role": "user",  # add user's question to messege_history
            "content": prompt,
        })

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=message_history,
        max_tokens=1024,  # chat 에서 생성해낼 수 있는 최대 tokens 수
        stop=None,  # 대화의 종류를 명시, None -> 종료 조건 x
        temperature=0.5,  # 0~2사이의 값, 높을 수록 더 랜덤한 response 발생, 낮을 수록 보다 정확한 정보 제공
    )

    message_history.append(
        {
            "role": "assistant",
            "content": response.choices[0].message.content,
        }
    )
    print("in chatbot method:", message_history[-1]["content"])


    return response.choices[0].message.content, message_history

@csrf_exempt
def request_to_chatbot(request):
    global message_history
    if request.method == "POST":
        prompt = str(request.POST.get("message"))
        response, updated_message_history = chatbot(prompt, message_history)
        print("in request to chatbot:", response)
        message_history = updated_message_history
        return JsonResponse({'reply': response})
    return JsonResponse({'error': 'Invalid request method'}, status=400)



