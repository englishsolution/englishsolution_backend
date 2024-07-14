from django.http import JsonResponse, HttpResponse

def test(request):
    if request.method == 'GET':
        return JsonResponse({"message","test"})