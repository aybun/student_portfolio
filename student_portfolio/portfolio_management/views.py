from django.shortcuts import render
#
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from student.models import Student
from staff.models import Staff

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

    groups = list(request.user.groups.values_list('name', flat=True))

    data_dict = {
        # 'is_staff' : 'staff' in groups,
        # 'is_student' : 'student' in groups,
        'groups' : groups,
    }


    if 'staff' in groups:
        staff = Staff.objects.get(userId=request.user.id)
        data_dict['staffId'] = staff.staffId

    elif 'student' in groups:
        student = Student.objects.get(userId=request.user.id)

        data_dict['studentId'] = student.studentId


    return JsonResponse(data_dict, safe=False)


def file(request, file_id):
    data_dict = {
        'file_id' : file_id,
    }
    return render(request, 'file/image.html', data_dict)


def fileApi(request):

    return None