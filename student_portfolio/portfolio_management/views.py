from django.shortcuts import render
#
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse


# from .models import Entry
# from .serializers import BlogAuthorSerializer
#
# from django.core.files.storage import default_storage
#
from user_profile.models import UserProfile


def home(request):

    stuff_for_frontend = {}

    return render(request, 'home/home.html', stuff_for_frontend)

def logoutView(request):

    return render(request, 'registration/error.html', {})

def userApi(request):

    groups = list(request.user.groups.values_list('name', flat=True))

    data_dict = {
        'is_staff' : 'staff' in groups,
        'is_student' : 'student' in groups,
        'groups' : groups,
    }

    user_profile = UserProfile.objects.get(user_id_fk=request.user.id)
    data_dict['uservisity_id'] = user_profile.university_id

    return JsonResponse(data_dict, safe=False)


def file(request, file_id):
    data_dict = {
        'file_id' : file_id,
    }
    return render(request, 'file/image.html', data_dict)


def fileApi(request):

    return None