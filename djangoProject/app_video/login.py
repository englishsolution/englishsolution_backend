from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        # 로그인 성공
        return Response({
            "success": True,
            "message": "Login successful",
            "user_id": user.id,
            "username": user.username
        }, status=status.HTTP_200_OK)
    else:
        # 로그인 실패
        return Response({
            "success": False,
            "message": "Invalid credentials"
        }, status=status.HTTP_401_UNAUTHORIZED)
