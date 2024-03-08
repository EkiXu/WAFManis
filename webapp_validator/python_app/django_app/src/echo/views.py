from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def echo(request):
    taint = request.POST.get('taint')
    id = request.POST.get('id')
    content_type = request.META.get("HTTP_CONTENT_TYPE")
    return JsonResponse({
        'form':{
            "taint":taint,
            "id":id,
        },
        'header':{
            "content-type":content_type
        }
    })
