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
def projectApi(request, projectId=0):

    groups = list(request.user.groups.values_list('name', flat=True))

    if request.method == 'GET':

        #Consider query params.
        if 'staff' in groups:
            if (projectId == 0):

                # projects = Project.objects.filter(approved__in=[False])
                projects = Project.objects.all()

                projects_serializer = ProjectSerializer(projects, many=True, context={'request': request})
                # print(projects_serializer.data)
                return JsonResponse(projects_serializer.data, safe=False)
            else:
                project = Project.objects.get(projectId=projectId)
                project_serializer = ProjectSerializer(project, context={'request': request})
                # print(event_serializer.data)
                return JsonResponse(project_serializer.data, safe=False)
        elif 'student' in groups:

            if (projectId == 0):
                projects = Project.objects.filter( Q(approved__in=[True]) | Q(proposed_by=request.user.id))

                # print(projects)
                project_serializer = ProjectSerializer(projects, many=True, context={'request': request})
                return JsonResponse(project_serializer.data, safe=False)
            else:
                project = Project.objects.get(projectId=projectId, proposed_by=request.user.id)
                project_serializer = ProjectSerializer(data=project, manay=False, context={'request': request})

                return JsonResponse(project_serializer.data, safe=False)


    elif request.method == 'POST':
        #Both staffs and non-staffs can proposed a project, so we need to record who approve the project.

        if 'staff' in groups:
            project_data = request.data.dict()
            project_data = ProjectSerializer.custom_clean(data=project_data, context={'request': request})
            serializer = ProjectSerializer(data=project_data, context={'request': request})

        elif 'student' in groups:
            project_data = request.data.dict()
            project_data = ProjectSerializer.custom_clean(data=project_data, context={'request': request})
            serializer = ProjectSerializer(data=project_data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        else:
            print(serializer.error_messages)
            print(serializer.errors)
            return JsonResponse("Failed to Add", safe=False)

    elif request.method == 'PUT':
        #Non-staff can edit the their proposed projects.

        if 'staff' in groups:
            project_data = request.data.dict()
            # print(project_data)
            project = Project.objects.get(projectId=projectId)
            # print(project)
            project_data = ProjectSerializer.custom_clean(instance=project, data=project_data, context={'request': request})
            serializer = ProjectSerializer(project, data=project_data, context={'request': request})

        elif 'student' in groups:
            project_data = request.data.dict()
            project = Project.objects.get(projectId=projectId, proposed_by=request.user.id)

            if (project.proposed_by == request.user.id) and not (project.approved):
                project_data = ProjectSerializer.custom_clean(instance=project, data=project_data, context={'request': request})
                serializer = ProjectSerializer(project, data=project_data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        else:
            print(serializer.error_messages)
            print(serializer.errors)
            return JsonResponse("Failed to Update", safe=False)


    elif request.method == 'DELETE':
        #Only staff can delete the approved project.

        project = Project.objects.get(projectId=projectId)
        if project is None:
            return JsonResponse("Failed to delete.", safe=False)

        proposed_by_the_user = (project.proposed_by == request.user.id)
        if 'staff' in groups or ('student' in groups and proposed_by_the_user and (not project.approved)):
            success = True
            try:
                with transaction.atomic():
                    project_delete_report = project.delete()

            except IntegrityError:
                # handle_exception
                success = False

            if success:
                return JsonResponse("Deleted Successfully", safe=False)
            else:
                return JsonResponse("Failed to delete.", safe=False)


