from http import HTTPStatus

from django.db import transaction, IntegrityError
from django.shortcuts import render
from django.http.response import JsonResponse
from django.db.models import Q

from rest_framework.decorators import parser_classes, api_view, permission_classes, authentication_classes, action
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .access_policies import *
from .serializers import *

from .models import Project
# Create your views here.

def project(request):

    return render(request, 'project/projects.html', {})

@parser_classes([JSONParser, MultiPartParser ])
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes((ProjectApiAccessPolicy,))
@authentication_classes((SessionAuthentication, BasicAuthentication))
def projectApi(request, project_id=0):

    Serializer = ProjectSerializer
    AccessPolicyClass = ProjectApiAccessPolicy
    Model = Project

    if request.method == "GET":
        if project_id == 0:
            query_object = AccessPolicyClass.scope_query_object(request=request)
            objects = Model.objects.filter(query_object).order_by('id')

            if not objects.exists():
                return JsonResponse([], safe=False)

            serializer = Serializer(objects, many=True, context={'request': request})
            # print(serializer.data)
            return JsonResponse(serializer.data, safe=False)
        else:
            id = project_id
            query_object = AccessPolicyClass.scope_query_object(request=request)
            object = Model.objects.filter(Q(id=id) & query_object).first()

            if object is None:
                return JsonResponse("The object does not exist.", safe=False, status=HTTPStatus.INTERNAL_SERVER_ERROR)

            serializer = Serializer(object, context={'request': request})
            return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = request.data.dict()
        # print(data)
        data = Serializer.custom_clean(data=data, context={'request': request})
        # print('{} {}'.format('after clean', data))

        serializer = Serializer(data=data, context={'request': request})

        if serializer.is_valid():
            success = True
            try:
                with transaction.atomic():
                    instance = serializer.save()
            except IntegrityError:
                success = False

            if success:
                request.method = 'GET'
                response_dict = {
                    'message' : "Added Successfully",
                    'data' : Serializer(instance=instance, context={'request': request}).data,
                }
                return JsonResponse(response_dict, safe=False)
            else:
                return JsonResponse("Failed to add.", safe=False, status=HTTPStatus.INTERNAL_SERVER_ERROR)

        else:
            print(serializer.error_messages)
            print(serializer.errors)
            return JsonResponse("Failed to Add", safe=False, status=HTTPStatus.INTERNAL_SERVER_ERROR)

    elif request.method == "PUT":
        id = project_id
        query_object = AccessPolicyClass.scope_query_object(request=request)
        object = Model.objects.filter(Q(id=id) & query_object).first()

        if object is None:
            return JsonResponse("Failed to update.", safe=False)

        data = request.data.dict()
        # print(data)
        data = Serializer.custom_clean(instance=object, data=data, context={'request': request})
        serializer = Serializer(object, data=data, context={'request': request})

        if serializer.is_valid():
            success = True
            try:
                with transaction.atomic():
                    instance = serializer.save()
            except IntegrityError:
                success = False
            if success:
                request.method = 'GET'
                response_dict = {
                    'message': "Added Successfully",
                    'data': Serializer(instance=instance, context={'request': request}).data,
                }
                return JsonResponse(response_dict, safe=False)
            else:
                return JsonResponse("Failed to delete.", safe=False)

        else:
            print(serializer.errors)
            print(serializer.error_messages)
            return JsonResponse("Failed to Update")

    elif request.method == "DELETE":
        id = project_id
        query_object = AccessPolicyClass.scope_query_object(request=request)
        object = Model.objects.filter(Q(id=id) & query_object).first()

        if object is None:
            return JsonResponse("Failed to delete.", safe=False)

        success = True
        try:
            with transaction.atomic():
                object.delete()
        except IntegrityError:
            success = False
        if success:
            return JsonResponse("Deleted Successfully", safe=False)
        else:
            return JsonResponse("Failed to delete.", safe=False)