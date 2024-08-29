from dotenv import load_dotenv
from openai import OpenAI
import os
from django.shortcuts import get_object_or_404
from ..models import Video

load_dotenv() #env 파일에서 api_key를 가져옴
API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY)

message_history=[]
last_video_title=''

def conversation_chatbot(request,video_title): #단어 chatbot

    global last_video_title
    global message_history

    if last_video_title!=video_title:
        message_history=[]
        last_video_title=video_title

    video = get_object_or_404(Video, title=video_title)
    video_script = video.script

    message_history.append(  # to consecutive message
        {
            "role": "user",  # add user's question to messege_history
            "content": request,
        })

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You're a machine being who talks about video topics. If I give you a caption of the video, you can watch it and talk to the user."
            },
            {
                "role": "user",
                "content": video_script  # 비디오 스크립트를 추가
            },
            *message_history  # 이전 대화 기록을 추가
        ],
        model="gpt-3.5-turbo",
        max_tokens=1024,
        temperature=1.2
    )

    # 응답 내용 추출
    response_message = response.choices[0].message.content

    # 대화 기록에 응답 추가
    message_history.append({
        "role": "assistant",
        "content": response_message
    })

    print(response.choices[0].message.content)
    return response.choices[0].message.content
