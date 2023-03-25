import csv
import io
from http import HTTPStatus

from django.db import transaction, IntegrityError
from django.db.models import Q
from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import parser_classes, permission_classes, api_view, authentication_classes
from rest_framework.parsers import JSONParser, MultiPartParser
from django.http.response import JsonResponse

from event.models import Curriculum
from .access_policies import UserProfileApiAccessPolicy, StaffApiAccessPolicy, StudentApiAccessPolicy, \
    CurriculumStudentBulkAddApiAccessPolicy
from .models import UserProfile
from .serializers import UserProfileSerializer, StudentSerializer, StaffSerializer, CurriculumStudentBulkAddSerializer


# Create your views here.


def info(request):

    return render(request, 'profile/info.html', {})


def charts(request):

    return render(request, 'profile/charts.html', {})

def editStudentProfile(request):

    return render(request, 'profile/edit_student_profile.html')

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
@api_view(['GET', 'PUT'])
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
            print(serializer.data)
            return JsonResponse(serializer.data, safe=False)
        else:
            id = userprofile_id
            query_object = AccessPolicyClass.scope_query_object(request=request)
            object = Model.objects.filter(Q(id=id) & Q(faculty_role__id=2) & query_object).first()

            if object is None:
                return JsonResponse("The object does not exist.", safe=False)

            serializer = Serializer(object, context={'request': request})
            return JsonResponse(serializer.data, safe=False)

    elif request.method=="PUT":
        id = userprofile_id
        query_object = AccessPolicyClass.scope_query_object(request=request)
        object = Model.objects.filter(Q(id=id) & Q(faculty_role__id=2) & query_object).first()

        if object is None:
            return JsonResponse("Failed to update.", safe=False)

        data = request.data.dict()
        data = Serializer.custom_clean(data=data, context={'request': request})
        serializer = Serializer(object, data=data, context={'request': request})
        # print(data)
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

def curriculumStudent(request, curriculum_id=0):
    stuff_for_frontend  = {
        'curriculum_id' : curriculum_id,
    }
    return render(request, 'profile/curriculum_student.html', stuff_for_frontend)

@parser_classes((MultiPartParser, JSONParser,))
@permission_classes((CurriculumStudentBulkAddApiAccessPolicy,))
@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
def curriculumStudentBulkAddApi(request):
    #Note : We have to ensure that every row is valid.

    data = request.data.dict()
    # print(data)
    serializer = CurriculumStudentBulkAddSerializer(data=data, context={'request': request})

    if not serializer.is_valid():
        print(serializer.error_messages)
        print(serializer.errors)
        response_dict = {
            'message': 'The serializer reject the input.',
        }
        return JsonResponse(data=response_dict, safe=False, status=HTTPStatus.INTERNAL_SERVER_ERROR)

    curriculum_id = serializer.validated_data['curriculum_id']
    csv_file = serializer.validated_data['csv_file']

    decoded_csv_file = csv_file.read().decode(encoding='utf-8-sig')
    io_string = io.StringIO(decoded_csv_file)
    csvreader = csv.reader(io_string, delimiter=',')

    header = next(csvreader)
    university_id_index = header.index('university_id')
    # university_ids = []
    invalid_rows = []
    valid_rows = []
    for (index, row) in enumerate(csvreader):

        temp_student = UserProfile.objects.filter(university_id=row[university_id_index], faculty_role=2).first()

        if temp_student is None:
            invalid_rows.append((index, row, 'university id does not exist.'))
        else:
            valid_rows.append(temp_student)

    if len(invalid_rows) != 0:
        response_dict = {
            'message': 'All rows must be valid but the file contains some invalid rows.',
            'invalid_rows': invalid_rows,
        }
        return JsonResponse(data=response_dict, safe=False, status=HTTPStatus.INTERNAL_SERVER_ERROR)

    #Save to the database.
    success = True
    curriculum = Curriculum.objects.get(id=curriculum_id)
    try:
        with transaction.atomic():
            for e in valid_rows:
                e.enroll = curriculum
                e.save()
    except IntegrityError:
        success = False

    if success:
        response_dict = {
            'message': 'Added Successfully. All rows are valid.',
        }
        return JsonResponse(data=response_dict, safe=False)
    else:
        response_dict = {
            'message': 'Failed to add.',
        }
        return JsonResponse(data=response_dict, safe=False, status=HTTPStatus.INTERNAL_SERVER_ERROR)


def eventAttendance(request):
    stuff_for_frontend = {

    }
    return render(request, 'profile/event_attendance.html', stuff_for_frontend)


# def skillChartDataApi(request):
#
#     user_id_fk = request.user.id
#
#
#     student_profile = UserProfile.objects.filter(user_id_fk=user_id_fk).first()
#
#     if student_profile is None:
#         return ''
#
#

