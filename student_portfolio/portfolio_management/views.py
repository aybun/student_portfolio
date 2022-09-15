from django.shortcuts import render
#
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
#
# from .models import Entry
# from .serializers import BlogAuthorSerializer
#
# from django.core.files.storage import default_storage
#

def home(request):

    stuff_for_frontend = {}

    return render(request, 'home/home.html', stuff_for_frontend)

def logoutView(request):

    return render(request, 'registration/error.html', {})

def userApi(request):
    data_dict = {
        'is_staff' : request.user.is_staff,
        'is_superuser': request.user.is_superuser,
    }

    return JsonResponse(data_dict, safe=False)


def file(request, file_id):
    data_dict = {
        'file_id' : file_id,
    }
    return render(request, 'file/image.html', data_dict)


def fileApi(request):

    return None