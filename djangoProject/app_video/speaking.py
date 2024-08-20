import os
import json
import urllib3
from django.http import JsonResponse
from django.shortcuts import render
from dotenv import load_dotenv

from openai import OpenAI

load_dotenv(verbose=True) #env 파일에서 api_key를 가져옴 # 배포시 verbose 지우기

ETRI_API_KEY=os.getenv("ETRI_API_KEY")

load_dotenv(verbose=True) #env 파일에서 api_key를 가져옴 # 배포시 verbose 지우기

API_KEY=os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=API_KEY)

def speaking(request):
    return render(request, 'app_video/speaking.html')

def sst(request):
    return render(request, 'app_video/sst.html')

def processing_sst(request):
    return render(request, 'app_video/sst.html')


def processing_speaking(request):
    if request.method == 'POST':
        print('processing_speaking 1st')
    # 문장 발음 기호
    script = "Nice to meet you!"
    request_content = f"Pronunciation of this sentence {script}"

    # ChatGPT 모델 호출 및 응답 받기
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": request_content}
        ],
        max_tokens=60,
        temperature=0.7
    )
    response_text = response.choices[0].message.content
    # 생성된 응답 출력
    print("발음기호 : ", response_text)

    print('processing_speaking')
    if request.method == 'POST' and 'audio' in request.FILES:
        print('test')
        # request.POST.get('audio')를 통해 데이터 가져오기
        audio_data = request.POST.get('audio')

        #audio_data_decoded  = base64.b64decode(audio_data).decode("utf8")

        # base64로 인코딩된 데이터를 디코딩하여 파일로 저장하거나 처리하는 예시
        try:
            openApiURL = 'http://aiopen.etri.re.kr:8000/WiseASR/Pronunciation'  # 영어
            accessKey = ETRI_API_KEY
            print(accessKey)
            languageCode = "english"
            script = "Nice to meet you!"

            requestJson = {
                "argument": {
                    "language_code": languageCode,
                    "script": script,
                    "audio": audio_data
                }
            }
            print('test2')
            http = urllib3.PoolManager()
            print('test3')
            response = http.request(
                "POST",
                openApiURL,
                headers={"Content-Type": "application/json; charset=UTF-8", "Authorization": accessKey},
                body=json.dumps(requestJson)
            )

            print("[responseCode] " + str(response.status))
            print("[responBody]")
            print(str(response.data, "utf-8"))
            return JsonResponse({'message': 'Audio file processed successfully.'})


        except Exception as e:
            print('error')
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method or no audio data received.'}, status=400)

