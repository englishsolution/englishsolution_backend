from django.shortcuts import render
from django.http import JsonResponse
from dotenv import load_dotenv
from openai import OpenAI
import os


load_dotenv() #env 파일에서 api_key를 가져옴
API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY)

general_message_history=[]  # 메세지의 연속성을 위해 과거 프롬프트 저장

def general_chatbot(prompt): #일반 chatbot
    global general_message_history

    if prompt == "exit":
        return "Exiting"

    general_message_history.append(  # to consecutive message
        {
            "role": "user",  # add user's question to messege_history
            "content": prompt,
        })

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=general_message_history,
        max_tokens=1024,  # chat 에서 생성해낼 수 있는 최대 tokens 수
        stop=None,  # 대화의 종류를 명시, None -> 종료 조건 x
        temperature=0.5,  # 0~2사이의 값, 높을 수록 더 랜덤한 response 발생, 낮을 수록 보다 정확한 정보 제공
    )

    general_message_history.append(
        {
            "role": "assistant",
            "content": response.choices[0].message.content,
        }
    )
    print("in chatbot method:", general_message_history[-1]["content"])

    return response.choices[0].message.content