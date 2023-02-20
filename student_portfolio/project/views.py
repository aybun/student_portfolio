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


# @parser_classes([JSONParser, MultiPartParser ])
# @api_view(['GET', 'POST', 'PUT', 'DELETE'])
# @permission_classes((ProjectApiAccessPolicy,))
# @authentication_classes((SessionAuthentication, BasicAuthentication))
# def projectApi(request, project_id=0):
#
#     groups = list(request.user.groups.values_list('name', flat=True))
#
#     if request.method == 'GET':
#
#         #Consider query params.
#         if 'staff' in groups:
#             if (project_id == 0):
#
#                 # projects = Project.objects.filter(approved__in=[False])
#                 projects = Project.objects.all()
#
#                 projects_serializer = ProjectSerializer(projects, many=True, context={'request': request})
#                 # print(projects_serializer.data)
#                 return JsonResponse(projects_serializer.data, safe=False)
#             else:
#                 project = Project.objects.get(projectId=project_id)
#                 project_serializer = ProjectSerializer(project, context={'request': request})
#                 # print(event_serializer.data)
#                 return JsonResponse(project_serializer.data, safe=False)
#         elif 'student' in groups:
#
#             if (project_id == 0):
#                 projects = Project.objects.filter( Q(approved__in=[True]) | Q(proposed_by=request.user.id))
#
#                 # print(projects)
#                 project_serializer = ProjectSerializer(projects, many=True, context={'request': request})
#                 return JsonResponse(project_serializer.data, safe=False)
#             else:
#                 project = Project.objects.get(projectId=project_id, proposed_by=request.user.id)
#                 project_serializer = ProjectSerializer(data=project, manay=False, context={'request': request})
#
#                 return JsonResponse(project_serializer.data, safe=False)
#
#
#     elif request.method == 'POST':
#         #Both staffs and non-staffs can proposed a project, so we need to record who approve the project.
#
#         if 'staff' in groups:
#             project_data = request.data.dict()
#             project_data = ProjectSerializer.custom_clean(data=project_data, context={'request': request})
#             serializer = ProjectSerializer(data=project_data, context={'request': request})
#
#         elif 'student' in groups:
#             project_data = request.data.dict()
#             project_data = ProjectSerializer.custom_clean(data=project_data, context={'request': request})
#             serializer = ProjectSerializer(data=project_data, context={'request': request})
#
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse("Added Successfully", safe=False)
#         else:
#             print(serializer.error_messages)
#             print(serializer.errors)
#             return JsonResponse("Failed to Add", safe=False)
#
#     elif request.method == 'PUT':
#         #Non-staff can edit the their proposed projects.
#
#         if 'staff' in groups:
#             project_data = request.data.dict()
#             # print(project_data)
#             project = Project.objects.get(projectId=project_id)
#             # print(project)
#             project_data = ProjectSerializer.custom_clean(instance=project, data=project_data, context={'request': request})
#             serializer = ProjectSerializer(project, data=project_data, context={'request': request})
#
#         elif 'student' in groups:
#             project_data = request.data.dict()
#             project = Project.objects.get(projectId=project_id, proposed_by=request.user.id)
#
#             if (project.proposed_by == request.user.id) and not (project.approved):
#                 project_data = ProjectSerializer.custom_clean(instance=project, data=project_data, context={'request': request})
#                 serializer = ProjectSerializer(project, data=project_data, context={'request': request})
#
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse("Updated Successfully", safe=False)
#         else:
#             print(serializer.error_messages)
#             print(serializer.errors)
#             return JsonResponse("Failed to Update", safe=False)
#
#
#     elif request.method == 'DELETE':
#         #Only staff can delete the approved project.
#
#         project = Project.objects.get(projectId=project_id)
#         if project is None:
#             return JsonResponse("Failed to delete.", safe=False)
#
#         proposed_by_the_user = (project.proposed_by == request.user.id)
#         if 'staff' in groups or ('student' in groups and proposed_by_the_user and (not project.approved)):
#             success = True
#             try:
#                 with transaction.atomic():
#                     project_delete_report = project.delete()
#
#             except IntegrityError:
#                 # handle_exception
#                 success = False
#
#             if success:
#                 return JsonResponse("Deleted Successfully", safe=False)
#             else:
#                 return JsonResponse("Failed to delete.", safe=False)


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
                return JsonResponse("The objects do not exist.", safe=False)

            serializer = Serializer(objects, many=True, context={'request': request})
            # print(serializer.data)
            return JsonResponse(serializer.data, safe=False)
        else:
            id = project_id
            query_object = AccessPolicyClass.scope_query_object(request=request)
            object = Model.objects.filter(Q(id=id) & query_object).first()

            if object is None:
                return JsonResponse("The object does not exist.", safe=False)

            serializer = Serializer(object, context={'request': request})
            return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = request.data.dict()
        data = Serializer.custom_clean(data=data, context={'request': request})
        serializer = Serializer(data=data, context={'request': request})

        if serializer.is_valid():
            success = True
            try:
                with transaction.atomic():
                    serializer.save()
            except IntegrityError:
                success = False

            if success:
                return JsonResponse("Added Successfully", safe=False)
            else:
                return JsonResponse("Failed to add.", safe=False)

        else:
            print(serializer.error_messages)
            print(serializer.errors)
            return JsonResponse("Failed to Add", safe=False)

    elif request.method == "PUT":
        id = project_id
        query_object = AccessPolicyClass.scope_query_object(request=request)
        object = Model.objects.filter(Q(id=id) & query_object).first()

        if object is None:
            return JsonResponse("Failed to update.", safe=False)

        data = request.data.dict()
        print(data)
        data = Serializer.custom_clean(instance=object, data=data, context={'request': request})
        serializer = Serializer(object, data=data, context={'request': request})


        if serializer.is_valid():
            success = True
            try:
                with transaction.atomic():
                    serializer.save()
            except IntegrityError:
                success = False
            if success:
                return JsonResponse("Updated Successfully", safe=False)
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