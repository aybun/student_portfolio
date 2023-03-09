import json

from django.contrib.auth.models import User
from django.shortcuts import render
#
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import parser_classes, permission_classes, api_view, authentication_classes
from rest_framework.parsers import JSONParser, MultiPartParser


from user_profile.models import UserProfile


def home(request):

    stuff_for_frontend = {}

    return render(request, 'home/home.html', stuff_for_frontend)

def logoutView(request):

    return render(request, 'registration/error.html', {})

def userApi(request):
    print(request.user.is_authenticated)
    groups = list(request.user.groups.values_list('name', flat=True))

    data_dict = {
        'is_staff' : 'staff' in groups,
        'is_student' : 'student' in groups,
        'groups' : groups,
        'id' : request.user.id,
        'is_authenticated': request.user.is_authenticated
    }

    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user_id_fk=request.user.id)
        data_dict['university_id'] = user_profile.university_id

    return JsonResponse(data_dict, safe=False)


@ensure_csrf_cookie
def get_csrf(request):
    response = JsonResponse({'detail': 'CSRF cookie set'})
    response['X-CSRFToken'] = get_token(request)
    return response

@authentication_classes((SessionAuthentication, BasicAuthentication))
@require_POST
def login_view(request):
    # data = json.loads(request.body)
    # username = data.get('username', None)
    # password = data.get('password', None)
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    print(request.POST)
    if username is None or password is None:
        return JsonResponse({'detail': 'Please provide username and password.'}, status=400)

    user = authenticate(username=username, password=password)

    if user is None:
        return JsonResponse({'detail': 'Invalid credentials.'}, status=400)

    login(request, user)
    return JsonResponse({'detail': 'Successfully logged in.'})


def logout_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'detail': 'You\'re not logged in.'}, status=400)

    logout(request)
    return JsonResponse({'detail': 'Successfully logged out.'})

@ensure_csrf_cookie
def session_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'isAuthenticated': False})

    return JsonResponse({'isAuthenticated': True})