import json

from django.db.models import F
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import Video

from dotenv import load_dotenv
from openai import OpenAI
import os

from youtube_transcript_api import YouTubeTranscriptApi
import re

import yt_dlp as youtube_dl

from django.contrib.auth.decorators import login_required

# Create your views here.

load_dotenv(verbose=True) #env 파일에서 api_key를 가져옴 # 배포시 verbose 지우기

API_KEY=os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=API_KEY)

@csrf_exempt
def processing_url(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError as e:
        return JsonResponse({'error': f'Invalid JSON format: {e}'}, status=400)

    if request.method == 'POST':
        url = data.get("url")
        user_id = data.get("user_id")
        if is_youtube_url(url) : #youtube 영상여부 체크
            video_id = get_youtube_video_id(url)
            if video_id != None : #video_id 추출
                # 자막 여부 체크

                try:
                    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                except json.JSONDecodeError as e:
                    print("자막 없음88888888888")
                    return JsonResponse({'error': '자막 없음'}, status=400)

                has_english = any(transcript.language_code == 'en' for transcript in transcript_list)
                has_korean = any(transcript.language_code == 'ko' for transcript in transcript_list)

                if has_english :
                    print('영어 자막 있음')#영어 자막 있는 경우
                    transcription_en = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
                else :
                    print('영어 자막 없음')#영어 자막 없는 경우
                    # YouTube에서 오디오 스트림 다운로드
                    audio_file_path = download_audio_yt_dlp(url, video_id)
                    # 오디오 파일 열기
                    audio_file = open(audio_file_path, "rb")

                    # Whisper API를 사용하여 오디오를 텍스트로 변환
                    response = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file,
                        response_format="verbose_json"  # 형식 start, end(srt는 00분 00초부터 00분 07초까지)
                    )
                    transcription_en=[]

                    for content in response.segments :
                        text = content['text']
                        start = content['start']
                        end = content['end']
                        duration = end - start
                        transcription_en.append({'text': text, 'start': start, 'duration': duration})

                script = ' '.join([content['text'] for content in transcription_en])
                script = separate_caption(script)

                # #한글자막 확인
                if has_korean:#한글 자막 있는 경우
                    print('한글 자막 있음')
                    transcription_ko = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko'])
                    script = ' '.join([content['text'] for content in transcription_ko])
                else :#한글 자막 없는 경우
                    print('한글 자막 없음')
                    #joined_text만 따로 번역
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {
                             "role": "system", "content": "You are a translation assistant."
                            },
                            {"role": "user", "content": f'{transcription_en} Please translate the \'text\' fields in the following JSON from English to Korean. Keep the \'start\' and \'duration\' fields unchanged. Return the result as a JSON object.'},
                        ],
                        temperature=0.7,
                        max_tokens= 4096,
                    )
                    # 응답에서 번역된 문장 추출
                    try :
                        transcription_ko = response.choices[0].message.content
                        transcription_ko = json.loads(transcription_ko)
                    except :
                        transcription_ko = '에러'
                        return JsonResponse({'error': '한글자막 에러'}, status=400)

                if not Video.objects.filter(user_id=user_id, video_identify=video_id).exists():

                    #title 정하기
                    request_content = f"Here is the video script: {script}. Based on this script, suggest a suitable title for the video. Do not use quotation marks"

                    # ChatGPT 모델 호출 및 응답 받기
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                         {"role": "user", "content": request_content}
                        ],
                        max_tokens=60,
                        temperature=0.7
                    )
                    title = response.choices[0].message.content
                    #img 정하기
                    thumbnail= 'https://img.youtube.com/vi/' + video_id + '/0.jpg'

                    #video 테이블에 저장
                    new_video_record = Video(
                        link=url,
                        title=title,
                        save_date=timezone.now(),
                        view_count=1,
                        img=thumbnail,
                        script=script,
                        user_id=user_id,
                        video_identify= video_id
                    ).save()

                else :
                    title = Video.objects.filter(user_id=user_id, video_identify=video_id).values_list('title', flat=True).first()
                    thumbnail = Video.objects.filter(user_id=user_id, video_identify=video_id).values_list('img', flat=True).first()

                return JsonResponse({'url': url,
                                        'title': title,
                                        'thumbnail': thumbnail,
                                        'script' : script,
                                        'transcription_ko':transcription_ko,
                                        'transcription_en': transcription_en})
    return render(request, 'app_video/insert_url.html')

def is_youtube_url(url):
    youtube_regex = re.compile(
        r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/' +
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    match = youtube_regex.match(url)
    return bool(match)

def get_youtube_video_id(url):
    if 'youtube.com' in url:
        return url.split('v=')[1].split('&')[0]
    elif 'youtu.be' in url:
        return url.split('/')[-1]
    else:
        return None


def download_audio_yt_dlp(youtube_url, video_id):
    output_path = f"audio_{video_id}"
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': output_path,
        'verbose': True  # 디버깅 정보를 더 많이 출력하도록 설정
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
        print(f"오디오 다운로드 완료: {output_path}")
        return output_path+'.mp3'
    except youtube_dl.utils.DownloadError as e:
        print(f"오디오 다운로드 중 오류 발생: {e}")
        return None
    except Exception as e:
        print(f"예기치 않은 오류 발생: {e}")
        return None

def separate_caption(script) :
    #문장으로 분리하기
    request_content = (f"I have a script that isn't properly separated into individual sentences. Could you please help me split the text into distinct sentences? Here is the script: {script}"
                       f"Please make sure to clearly separate each sentence by period and include punctuation marks or capital letters. Do not use quotation marks. Do not use newline characters. Treat special phrases or non-standard punctuation marks such as [Music] or [Applause] as separate sentences and separate them with a period.")

    # ChatGPT 모델 호출 및 응답 받기
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": request_content}
        ],
        max_tokens=1000,
        temperature=0.6
    )
    response_text = response.choices[0].message.content
    # 생성된 응답 출력
    return response_text
