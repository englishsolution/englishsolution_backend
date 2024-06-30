from django.shortcuts import render
from .models import Test

# Create your views here.
def test(request):
    tests = Test.objects.all()
    return render(request, 'index.html', {"tests":tests})