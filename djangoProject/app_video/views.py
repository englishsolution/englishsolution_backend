from django.shortcuts import render
from .models import test

# Create your views here.
def test(request):
    tests = test.objects.all()
    return render(request, 'index.html', {"tests":tests})