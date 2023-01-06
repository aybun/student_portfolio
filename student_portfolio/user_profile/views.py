from django.db.models import Q
from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import parser_classes, permission_classes, api_view, authentication_classes
from rest_framework.parsers import JSONParser, MultiPartParser
from django.http.response import JsonResponse

from .access_policies import UserProfileApiAccessPolicy, StaffApiAccessPolicy, StudentApiAccessPolicy
from .models import UserProfile
from .serializers import UserProfileSerializer, StudentSerializer, StaffSerializer


# Create your views here.


def info(request):

    return render(request, 'profile/info.html', {})


def charts(request):

    return render(request, 'profile/charts.html', {})

@parser_classes([JSONParser, MultiPartParser])
@permission_classes((StaffApiAccessPolicy,))
@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
def staffApi(request, userprofile_id=0):
    Serializer = StaffSerializer
    AccessPolicyClass = StaffApiAccessPolicy
    Model = UserProfile

    if request.method=='GET':
        if userprofile_id == 0:
            query_object = AccessPolicyClass.scope_query_object(request)
            staffs = Model.objects.filter(Q(faculty_role__id=1) & query_object)
            serializer = Serializer(staffs, many=True, context={'request': request})

            return JsonResponse(serializer.data, safe=False)
        else:

            id = userprofile_id
            query_object = AccessPolicyClass.scope_query_object(request=request)
            object = Model.objects.filter(Q(id=id) & Q(faculty_role__id=1) & query_object).first()

            if object is None:
                return JsonResponse("The object does not exist.", safe=False)

            serializer = Serializer(object, context={'request': request})
            return JsonResponse(serializer.data, safe=False)


@parser_classes([JSONParser, MultiPartParser])
@permission_classes((StudentApiAccessPolicy,))
@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
def studentApi(request, userprofile_id=0):
    Serializer = StudentSerializer
    AccessPolicyClass = StudentApiAccessPolicy
    Model = UserProfile

    if request.method=='GET':
        if userprofile_id == 0:
            query_object = AccessPolicyClass.scope_query_object(request)
            objects = Model.objects.filter(Q(faculty_role__id=2) & query_object)
            serializer = Serializer(objects, many=True, context={'request': request})
            return JsonResponse(serializer.data, safe=False)
        else:
            id = userprofile_id
            query_object = AccessPolicyClass.scope_query_object(request=request)
            object = Model.objects.filter(Q(id=id) & Q(faculty_role__id=2) & query_object).first()

            if object is None:
                return JsonResponse("The object does not exist.", safe=False)

            serializer = Serializer(object, context={'request': request})
            return JsonResponse(serializer.data, safe=False)


@parser_classes([JSONParser, MultiPartParser])
@permission_classes((UserProfileApiAccessPolicy,))
@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
def profileApi(request, userprofile_id=0):

    Serializer = UserProfileSerializer
    AccessPolicyClass = UserProfileApiAccessPolicy
    Model = UserProfile
    if request.method == "GET":

        if userprofile_id == 0:
            query_object = AccessPolicyClass.scope_query_object(request=request)
            objects = Model.objects.filter(query_object).order_by('id')

            if not objects.exists():
                return JsonResponse("The objects do not exist.", safe=False)

            serializer = Serializer(objects, many=True, context={'request': request})
            # print(serializer.data)
            return JsonResponse(serializer.data, safe=False)
        else:
            id = userprofile_id
            query_object = AccessPolicyClass.scope_query_object(request=request)
            object = Model.objects.filter(Q(id=id) & query_object).first()

            if object is None:
                return JsonResponse("The object does not exist.", safe=False)

            serializer = Serializer(object, context={'request': request})
            return JsonResponse(serializer.data, safe=False)