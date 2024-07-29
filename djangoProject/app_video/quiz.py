import json

from django.shortcuts import render
from dotenv import load_dotenv
from openai import OpenAI
import os

from app_video.models import Video, Sentence
from django.db.models.functions import Random

load_dotenv(verbose=True) #env 파일에서 api_key를 가져옴 # 배포시 verbose 지우기

API_KEY=os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=API_KEY)

def select_quiz(request):
    videos = Video.objects.all()
    return render(request, 'app_video/select_quiz.html', {"videos": videos})

def all_sentence_quiz(request):
    if request.method == 'POST':
        #문장이 없는 경우
        count=Sentence.objects.count()
        if(count==0):
            print('문장 없음~~')
            return render(request, 'app_video/select_quiz.html', {
            })
        elif (count<=10):
            print('<=10')
            sentence_list=Sentence.objects.values_list('sentence_eg', flat=False)
            sentences= " / ".join(sentence_list)
            print(sentences)
        elif (count>10):
            print('>10')
            random_sentence_list = Sentence.objects.order_by(Random()).values_list('sentence_eg', flat=True)[:10]
            sentences = " / ".join(random_sentence_list)
            print(sentences)

        request_content = (f"Five sentences: {sentences}.Purpose: Fill in the blanks. "
                           f"You're a great blank-making problem maker. For each sentence, you create a problem by specifying an important word or vocabulary as a blank and changing it to '__'."
                            f"Answer with JSON in the form of \'Question\', \'answer\'")

        # ChatGPT 모델 호출 및 응답 받기
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": request_content}
            ],
            max_tokens=1000,
            temperature=0.8,
            # response_format 지정하기
            response_format = {"type": "json_object"}
        )

        response_text = response.choices[0].message.content
        json_quiz = json.loads(response_text)

        return render(request, 'app_video/select_quiz.html', {
                {"json_quiz": json_quiz}
        })