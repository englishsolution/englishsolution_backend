import json
from datetime import datetime

import openai
from django.http import HttpResponse
from django.shortcuts import render, redirect
from moviepy.audio.io.AudioFileClip import AudioFileClip
from pytube import YouTube

from .models import Test
from .models import Video

from dotenv import load_dotenv
from openai import OpenAI
import os

from youtube_transcript_api import YouTubeTranscriptApi
import re


# Create your views here.

load_dotenv(verbose=True) #env 파일에서 api_key를 가져옴 # 배포시 verbose 지우기

API_KEY=os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=API_KEY)

def test(request):
    tests = Test.objects.all()
    return render(request, 'app_video/index.html', {"tests":tests})

def insert_url(request):
    return render(request, 'app_video/insert_url.html')

def processing_url(request):
    print("url_link_start")
    if request.method == 'POST':
        url = request.POST['url']
        print(url)
        if is_youtube_url(url) : #youtube 영상여부 체크
            video_id = get_youtube_video_id(url)
            print(video_id)
            script=''
            if video_id != None : #video_id 추출
                # 자막 여부 체크
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                has_english = any(transcript.language_code == 'en' for transcript in transcript_list)
                has_korean = any(transcript.language_code == 'ko' for transcript in transcript_list)
                transcription_en=[]
                transcription_ko=[]
                if has_english :
                    print('영어 자막 있음')#영어 자막 있는 경우
                    transcription_en = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
                    print(transcription_en)
                    script = ' '.join([content['text'] for content in transcription_en])
                    print(script)
                else :
                    print('영어 자막 없음')
                    #영어 자막 없는 경우
                    # YouTube에서 오디오 스트림 다운로드
                    yt = YouTube(url)
                    stream = yt.streams.filter(only_audio=True).first()
                    audio_file_path = stream.download(filename='audio.mp4')

                    # 오디오 파일 열기
                    audio_file = open(audio_file_path, "rb")

                    # Whisper API를 사용하여 오디오를 텍스트로 변환
                    response = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file,
                        response_format="verbose_json"  # 형식 start, end(srt는 00분 00초부터 00분 07초까지)
                    )

                    script = response.text
                    transcription_en=[]
                    for content in response.segments :
                        text = content['text']
                        start = content['start']
                        end = content['end']
                        duration = end - start
                        transcription_en.append({'text': text, 'start': start, 'duration': duration})
                    print(transcription_en)

                #한글자막 확인
                if None:
                    print('한글 자막 있음') #한글 자막 있는 경우
                    transcription_ko = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko'])
                    script = ' '.join([content['text'] for content in transcription_ko])
                    print(script)
                else :
                    print('한글 자막 없음')

                    #joined_text만 따로 번역
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "user", "content": f'{transcription_en} Translate only the values corresponding to \'text\' into Korean ah its getting so laid"'},
                        ],
                        temperature=0.7
                    )
                    # 응답에서 번역된 문장 추출
                    print('응답에서 번역된 문장 추출')
                    transcription_ko = response.choices[0].message.content

                #title 정하기
                request_content = f"Here is the video script: {script}. Based on this script, suggest a suitable title for the video."

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
                print("title : ", response_text)

                #img 정하기
                thumbnail= 'https://img.youtube.com/vi/' + video_id + '/0.jpg'
                print(thumbnail)

                #video 테이블에 저장
                new_video_record = Video(
                    user_id='user1',
                    link=url,
                    title=response_text,
                    save_date=datetime.now(),
                    view_count=1,
                    img=thumbnail,
                    script=script
                )
                new_video_record.save()

                return render(request, 'app_video/res.html', {
                    'url':url,
                    'title': response_text,
                    'thumbnail': thumbnail,
                })
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