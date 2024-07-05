from django.http import JsonResponse, HttpResponse

def test(request):
    return HttpResponse("hello world!")