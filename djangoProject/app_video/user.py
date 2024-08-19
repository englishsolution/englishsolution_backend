from django.contrib.auth import authenticate
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt
import json

from .tokens import account_activation_token

@csrf_exempt
def signup(request):
    data = json.loads(request.body.decode('utf-8'))
    if request.method == 'POST':
        username = data.get('username')
        first_name = data.get('firstname')
        last_name = data.get('last_name')
        email = data.get('email')
        password1 = data.get('password1')
        password2 = data.get('password2')

        if password1 == password2:
            if User.objects.filter(email=email).exists():
                print('이메일 존재함')
                return JsonResponse({'error': 'No valid response generated'}, status=400)
            user = User.objects.create_user(username=username, first_name=first_name, last_name = last_name, email=email, password=password1)
            user.is_active = False  # 계정을 비활성화 상태로 생성

            user.save()

            current_site = get_current_site(request)
            subject = '계정 활성화 링크입니다.'
            message = render_to_string('app_video/activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            email_message = EmailMessage(subject, message, to=[email])
            email_message.send()

            return JsonResponse({'username': username,
                                 'email': email})

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def activate(request, uidb64, token):
    """
    계정 활성화 뷰
    """
    try:
        # URL로부터 사용자 ID를 디코딩
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_object_or_404(User, pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # 토큰 검증
    if user is not None and account_activation_token.check_token(user, token):
        if user.is_active:
            return HttpResponse('계정이 이미 활성화되었습니다.')
        else:
            user.is_active = True
            user.state = 0
            user.save()
            return HttpResponse('이메일 인증 완료되었습니다.')
    else:
        return HttpResponse('유효하지 않은 활성화 링크입니다.')

@csrf_exempt
def check_id(request):
    data = json.loads(request.body.decode('utf-8'))
    if request.method == 'POST':
        username = data.get('username')
        try :
            user = User.objects.get(username=username)
        except Exception as e:
            user = None
        result = {
            'result' : "not exist" if user is None else "exist"
        }
        return JsonResponse(result)
    JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def login(request):
    data = json.loads(request.body.decode('utf-8'))
    if request.method == 'POST':
        username =  data.get('username')
        request.session['username'] = username
        return JsonResponse({'username': username})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def logout(request):
    data = json.loads(request.body.decode('utf-8'))
    if request.method == 'POST':
        username = data.get('username')
        try:
            print('삭제 후')
            request.session.modified = True  # 세션 삭제 가능하도록 등록
            del request.session['username']  # 세션 삭제
            return JsonResponse({'username': username})
        except:
            pass
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def delete(request):
    data = json.loads(request.body.decode('utf-8'))
    if request.method == 'POST':
        username = data.get('username')
        password = data.get('password')
        try:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # request.session.modified = True  # 세션 삭제 가능하도록 등록
                # del request.session['username']  # 세션 삭제
                # 탈퇴 처리
                user.state = 1
                user.save()
                return JsonResponse({'message': '탈퇴 완료'})
            else:
                # 인증에 실패하면 에러 메시지 표시
                return JsonResponse({'error': 'password not match'}, status=500)
        except:
            pass

    return JsonResponse({'error': 'Invalid request method'}, status=400)

