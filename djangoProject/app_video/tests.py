from django.test import TestCase
from django.utils import timezone
from django.http import JsonResponse, request, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
# Create your tests here.
@csrf_exempt
def request_to_chatbot(request):  # chatbot 요청을 처리하는 함수
    if request.method == "POST":
        try:
            print(1)
            data = json.loads(request.body.decode('utf-8'))
            print(2)
            mode = data.get("mode")
            print(3)
            prompt = data.get("prompt")
            print(4)
            return JsonResponse({'mode': mode,
                                 'prompt': prompt})
        except ValueError as ve:
            # 예외: 잘못된 입력값
            return JsonResponse({'error': str(ve)}, status=400)

