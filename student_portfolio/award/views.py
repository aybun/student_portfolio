import json
import os
from copy import deepcopy

from django.db import IntegrityError, transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import parser_classes, permission_classes, api_view, authentication_classes
from rest_framework.parsers import JSONParser, MultiPartParser

from award.access_policies import AwardApiAccessPolicy
from award.models import Award
from award.serializers import AwardSerializer


def _delete_file(path):
   """ Deletes file from filesystem. """
   if os.path.isfile(path):
       os.remove(path)

def award(request):
    return render(request, 'award/award.html', {})


@parser_classes([JSONParser, MultiPartParser])
@permission_classes((AwardApiAccessPolicy,))
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
def awardApi(request, award_id=0):

    Serializer = AwardSerializer
    AccessPolicyClass = AwardApiAccessPolicy
    Model = Award

    if request.method == "GET":
        if award_id == 0:
            query_object = AccessPolicyClass.scope_query_object(request=request)
            objects = Model.objects.filter(query_object).distinct('id').order_by('id')

            if not objects.exists():
                return JsonResponse([], safe=False)

            serializer = Serializer(objects, many=True, context={'request': request})
            # print(serializer.data)
            return JsonResponse(serializer.data, safe=False)
        else:
            id = award_id
            query_object = AccessPolicyClass.scope_query_object(request=request)
            object = Model.objects.filter(Q(id=id) & query_object).first()

            if object is None:
                return JsonResponse("The object does not exist.", safe=False)

            serializer = Serializer(object, context={'request': request})
            return JsonResponse(serializer.data, safe=False)
    elif request.method == "POST":
        data = request.data.dict()
        object, data = Serializer.custom_clean(data=data, context={'request': request})
        serializer = Serializer(data=data, context={'request': request})
        # print(data)
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
        id = award_id
        query_object = AccessPolicyClass.scope_query_object(request=request)
        object = Model.objects.filter(Q(id=id) & query_object).first()
        # print(object.approved_by)
        if object is None:
            return JsonResponse("Failed to update.", safe=False)
        old_obj = deepcopy(object) # old_obj : We want the paths of files to be deleted.

        data = request.data.dict()

        object, data = Serializer.custom_clean(instance=object, data=data, context={'request': request})
        print(data)
        serializer = Serializer(instance=object, data=data, context={'request': request})

        if serializer.is_valid():
            success = True
            try:
                with transaction.atomic():
                    serializer.save()
            except IntegrityError:
                success = False

            # Delete Files
            if success:
                #Check if the file field passed is ''. or the new file is passed -> Remove the old file.

                if old_obj.attachment_file and not bool(object.attachment_file)\
                        or old_obj.attachment_file != object.attachment_file:
                    _delete_file(str(old_obj.attachment_file))

            # Sending Messages
            if success:
                # We want to get the data.
                request.method="GET"
                return JsonResponse(Serializer(instance=object, context={'request' : request}).data, safe=False)
            else:
                return JsonResponse("Failed to delete.", safe=False)

        else:
            print(serializer.errors)
            print(serializer.error_messages)
            return JsonResponse("Failed to Update")

    elif request.method == "DELETE":
        id = award_id
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

@parser_classes([JSONParser, MultiPartParser])
@permission_classes((AwardApiAccessPolicy,))
@api_view(['DELETE'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
def awardApiMultiDelete(request):

    data = request.data.dict()
    print(data)
    ids = json.loads(data['ids'])
    query_object = AwardApiAccessPolicy.scope_query_object(request=request)
    objects = Award.objects.filter(Q(id__in=ids) & query_object)

    success = True
    try:
        with transaction.atomic():
            objects.delete()
    except IntegrityError:
        success = False
    if success:
        return JsonResponse("Deleted Successfully", safe=False)
    else:
        return JsonResponse("Failed to delete.", safe=False)