# import django.db.transaction
import csv
import io

from django.shortcuts import render
from django.db import IntegrityError, transaction
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.db.models import Q
from django.contrib.auth.models import User

# from student.models import Student
from user_profile.models import UserProfile
from .models import Event, EventAttendance, Skill, Curriculum, Skillgroup
from .serializers import EventSerializer, SkillSerializer, EventSkillSerializer, EventAttendanceSerializer, \
    CurriculumSerializer, SkillGroupSerializer, EventAttendanceBulkAddSerializer

from rest_framework.decorators import parser_classes, api_view, permission_classes, authentication_classes, action
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


from .access_policies import *


import json

# Create your views here.
def event(request, id=0):

    if not request.user.is_authenticated:
        return render(request, 'home/error.html', {'error_message': 'The user has no permission to access.'})

    return render(request, 'event/event.html', {})



@parser_classes([JSONParser, MultiPartParser ])
@permission_classes((EventApiAccessPolicy,))
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
def eventApi(request, event_id=0):

    groups = list(request.user.groups.values_list('name', flat=True))

    if request.method=='GET':

        if ('staff' in groups) or ('student' in groups):
            if (event_id == 0):
                query_object = EventApiAccessPolicy.scope_query_object(request=request)
                events = Event.objects.filter(query_object).order_by('id')

                if not events.exists():
                    return JsonResponse({}, safe=False)

                event_serializer = EventSerializer(events, many=True, context={'request': request})
                # print(event_serializer.data)
                return JsonResponse(event_serializer.data, safe=False)
            else:

                query_object = EventApiAccessPolicy.scope_query_object(request=request)
                event = Event.objects.filter(Q(id=event_id) & query_object).first()

                if event is None:
                    return JsonResponse("The object does not exist.", safe=False)

                event_serializer = EventSerializer(event, context={'request' : request})

                return JsonResponse(event_serializer.data, safe=False)

        # elif 'student' in groups:
        #     if (event_id == 0):
        #         student = Student.objects.get(userId=request.user.id)
        #         events_joined_by_user = list(EventAttendanceOfStudents.objects.filter(studentId__exact=student.studentId).values_list('eventId', flat=True))
        #         events = Event.objects.filter(Q(eventId__in=events_joined_by_user) | Q(created_by=request.user.id))
        #
        #         serializer=EventSerializer(events, many=True, context={'request' : request})
        #         return JsonResponse(serializer.data, safe=False)
        #     else:
        #         student = Student.objects.get(userId=request.user.id)
        #         event_attended = EventAttendanceOfStudents.objects.filter(studentId__exact=student.studentId, id=event_id)
        #
        #         if event_attended is not None:
        #             event = Event.objects.get(id=event_id)
        #             serializer = EventSerializer(event, context={'request': request})
        #             return JsonResponse(serializer.data, safe=False)
        #         else:
        #             return JsonResponse("Event not found.", safe=False)



    elif request.method=='POST':

        if 'staff' in groups or 'student' in groups:

            event_data = request.data.dict()
            event_data = EventSerializer.custom_clean(data=event_data, context={'request':request})
            event_serializer = EventSerializer(data=event_data, context={'request':request})

            if event_serializer.is_valid():

                success = True
                try:
                    with transaction.atomic():
                        event_serializer.save()
                except IntegrityError:
                    success = False
                if success:
                    return JsonResponse("Added Successfully", safe=False)
                else:
                    return JsonResponse("Failed to add.", safe=False)

            else:
                print(event_serializer.error_messages)
                print(event_serializer.errors)
                return JsonResponse("Failed to Add", safe=False)

    elif request.method=='PUT':

        if 'staff' in groups or 'student' in groups:

            query_object = EventApiAccessPolicy.scope_query_object(request=request)
            event = Event.objects.filter(Q(id=event_id) & query_object).first()
            if event is None:
                return JsonResponse("Failed to update.", safe=False)

            data = request.data.dict()
            print(data)
            event_data = EventSerializer.custom_clean(instance=event, data=data, context={'request' : request})
            event_serializer = EventSerializer(event, data=event_data, context={'request': request})

            if event_serializer.is_valid():

                success = True
                try:
                    with transaction.atomic():
                        event_serializer.save()

                except IntegrityError:

                    success = False

                if success:
                    return JsonResponse("Updated Successfully", safe=False)
                else:
                    return JsonResponse("Failed to delete.", safe=False)

            else:
                print(event_serializer.errors)
                print(event_serializer.error_messages)
                return JsonResponse("Failed to Update")

    elif request.method=='DELETE':

        if 'staff' in groups or 'student' in groups:

            query_object = EventApiAccessPolicy.scope_query_object(request=request)
            event = Event.objects.filter(Q(id=event_id) & query_object).first()

            if event is None:
                return JsonResponse("Failed to delete.", safe=False)

            success = True
            try:
                with transaction.atomic():
                    event.delete()
            except IntegrityError:
                success=False
            if success:
                return JsonResponse("Deleted Successfully", safe=False)
            else:
                return JsonResponse("Failed to delete.", safe=False)

def eventAttendanceOfStudents(request, event_id=0):

    groups = list(request.user.groups.values_list('name', flat=True))

    if 'staff' in groups:

        stuff_for_frontend = { 'event_id' : event_id }
        return render(request, 'event/event_attendance_of_students.html', stuff_for_frontend)
    else:
        return render(request, 'home/error.html', {'error_message': 'The user has no permission to access.'})


@parser_classes((JSONParser,))
@permission_classes((EventAttendanceApiAccessPolicy,))
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
def eventAttendanceApi(request, event_id=0, attendance_id=0):

    groups = list(request.user.groups.values_list('name', flat=True))

    if request.method=='GET':
        if 'staff' in groups:
            if (attendance_id == 0):

                query_object = EventAttendanceApiAccessPolicy.scope_query_object(request=request)
                attendances = EventAttendance.objects.filter( Q(event_id_fk=event_id) & query_object ).order_by('id')
                serializer = EventAttendanceSerializer(attendances, many=True, context={'request' : request})

                return JsonResponse(serializer.data, safe=False)
            else:
                query_object = EventAttendanceApiAccessPolicy.scope_query_object(request=request)
                attendance = EventAttendance.objects.filter(Q(id=attendance_id) & query_object).first()

                if attendance is None:
                    return JsonResponse("The object does not exist.", safe=False)

                serializer = EventAttendanceSerializer(attendance, context={'request' : request})
                return JsonResponse(serializer.data, safe=False)


        # elif 'student' in groups:
        #     # student = Student.objects.get(user_id_fk=request.user.id)
        #     attendances = EventAttendance.objects.filter(user_id_fk=request.user.id)
        #
        #     if not attendances.exists():
        #         return JsonResponse("The objects do not exist.", safe=False)
        #
        #     event_id_list = attendances.values_list('event_id_fk', flat=True)
        #
        #     events = Event.objects.filter(id__in=event_id_list)
        #
        #     if events.exists():
        #         event_serializer = EventSerializer(events, many=True, context={'request': request})
        #         return JsonResponse(event_serializer.data, safe=False)
        #     else:
        #         return JsonResponse("The objects do not exist.", safe=False)

    elif request.method=='POST':
        if 'staff' in groups:

            attendance_data = request.data.dict()
            # print(attendance_data)
            attendance = EventAttendance.objects.filter(event_id_fk=attendance_data['event_id_fk'],
                                                        university_id=attendance_data['university_id'])

            if not attendance.exists():
                serializer = EventAttendanceSerializer(data=attendance_data, context={'request' : request})
            else:
                return JsonResponse("The student is present in the attendance table.", safe=False)

            if serializer.is_valid():
                serializer.save()
                return JsonResponse("Added Successfully", safe=False)
            else:
                print(serializer.error_messages)
                print(serializer.errors)
                return JsonResponse("Failed to Add", safe=False)

    elif request.method=='PUT':

        if 'staff' in groups:
            attendance_data = request.data.dict()

            attendance_data = EventAttendanceSerializer.custom_clean(data=attendance_data, context={'request' : request})

            # print(attendance_data)
            attendance = EventAttendance.objects.filter(id=attendance_data['id']).first()
            if attendance is None:
                return JsonResponse("Failed to Update", safe=False)

            serializer=EventAttendanceSerializer(attendance, data=attendance_data, context={'request' : request})

            if serializer.is_valid():
                serializer.save()
                return JsonResponse("Updated Successfully",safe=False)
            else:
                print(serializer.error_messages)
                print(serializer.errors)
                return JsonResponse("Failed to Update", safe=False)

    elif request.method=='DELETE': #Need to handle carefully.

        if 'staff' in groups:
            attendance = EventAttendance.objects.get(id=attendance_id)

            if attendance is not None:
                attendance.delete()
                return JsonResponse("Deleted Successfully", safe=False)
            else:
                return JsonResponse("Object not found", safe=False)


@parser_classes([JSONParser, MultiPartParser])
@permission_classes((EventAttendedListApiAccessPolicy,))
@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
def eventAttendedListApi(request, user_id=0):
    Serializer = EventSerializer
    AccessPolicyClass = EventAttendedListApiAccessPolicy
    Model = Event

    Serializer.Meta.access_policy = AccessPolicyClass
    if request.method == "GET":
        if user_id == 0:
            query_object = AccessPolicyClass.scope_query_object(request=request)
            objects = Model.objects.filter(query_object).order_by('id')

            if not objects.exists():
                return JsonResponse("The objects do not exist.", safe=False)


            serializer = Serializer(objects, many=True, context={'request': request})

            # print(serializer.data)
            return JsonResponse(serializer.data, safe=False)


@parser_classes((MultiPartParser, JSONParser,))
@permission_classes((EventAttendanceBulkAddApiAccessPolicy,))
@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
def eventAttendanceBulkAddApi(request):

    data = request.data.dict()
    serializer = EventAttendanceBulkAddSerializer(data=data, context={'request': request})

    if serializer.is_valid():

        event_id = serializer.validated_data['event_id']
        csv_file = serializer.validated_data['csv_file']

        decoded_csv_file = csv_file.read().decode(encoding='utf-8-sig')
        io_string = io.StringIO(decoded_csv_file)
        csvreader = csv.reader(io_string, delimiter=',')

        valid_serializers = []
        invalid_rows = []

        header = next(csvreader)
        # print(header)
        for (index, row) in enumerate(csvreader):
            # print(row)
            temp_dict = {'event_id_fk': event_id}
            for (col_label, col) in zip(header, row):
                temp_dict[col_label] = col
                # print(temp_dict)
            attendance_serializer = EventAttendanceSerializer(data=temp_dict, context={'request': request})

            if attendance_serializer.is_valid():
                valid_serializers.append(attendance_serializer)

            else: #Note : Send out the invalid row.
                invalid_rows.append((index, row))

        success = True
        try:
            with transaction.atomic():
                for e in valid_serializers:
                    e.save()
        except IntegrityError:
            success = False

        if success:
            return JsonResponse("Added Successfully.", safe=False)
        else:
            return JsonResponse("Failed to add.", safe=False)

    else:
        print(serializer.error_messages)
        print(serializer.errors)
        return JsonResponse("Failed to add.", safe=False)


@parser_classes((JSONParser, MultiPartParser))
@permission_classes((EventAttendanceApiAccessPolicy,))
@api_view(['PUT'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
def syncAttendanceByUniversityId(request, event_id=0):

    if request.method == 'PUT':

        #Make queries.
        attendances = EventAttendance.objects.filter(event_id_fk=event_id)
        university_id_list_of_attendees = attendances.values_list('university_id', flat=True)
        first_two_letters_set = set([e[:2] for e in university_id_list_of_attendees])
        query_string = Q()
        for e in first_two_letters_set:
            query_string = query_string | Q(university_id__startswith=e)

        user_profiles = UserProfile.objects.filter(query_string).values_list('university_id', 'user_id_fk')

        university_ids = [e[0] for e in user_profiles]
        user_id_fks = [e[1] for e in user_profiles]

        #Delete Duplications.
        to_be_saved = []
        unique_user_ids = []
        for attendance in attendances:
            if attendance.university_id not in unique_user_ids:
                unique_user_ids.append(attendance.university_id)
                to_be_saved.append(attendance)
            else:
                attendance.delete()

        #Set synced=True and Set user_id_fk.
        attendances = to_be_saved
        for attendance in attendances:
            for i in range(0, len(university_ids)):
                if attendance.university_id == university_ids[i]:
                    attendance.synced = True
                    attendance.user_id_fk = User.objects.get(id=user_id_fks[i])

        #Save to the database.
        success = True
        try:
            with transaction.atomic():
                for attendance in attendances:
                    attendance.save()

        except IntegrityError:
            success = False

        if success:
            return JsonResponse("Synced Successfully", safe=False)
        else:
            return JsonResponse("Failed to sync.", safe=False)


@parser_classes([JSONParser, MultiPartParser])
@api_view(['GET', 'PUT'])
@permission_classes((SkillTableApiAccessPolicy,))
@authentication_classes((SessionAuthentication, BasicAuthentication))
def skillTableApi(request):

    if request.method == 'GET':
        skill_table = Skill.objects.all().order_by('id')
        serializer = SkillSerializer(skill_table, many=True)
        return JsonResponse(serializer.data, safe=False)
    if request.method == 'PUT':

        skillTable_data = JSONParser().parse(request)
        skillTable_data = sorted(skillTable_data, key=lambda x: x['id'])

        skills = Skill.objects.all().order_by('id')
        # print(skills)
        # print(skillTable_data)
        # print("Bye")

        with transaction.atomic():
            for i in range(0, len(skills)):
                serializer = SkillSerializer(skills[i], data=skillTable_data[i])

                if serializer.is_valid():
                    serializer.save()
                else:
                    print(serializer.error_messages)
                    print(serializer.errors)
                    return JsonResponse("Failed to Update", safe=False)

        return JsonResponse("Updated Successfully", safe=False)


def curriculum(request):
    return render(request, 'profile/curriculum.html', {})

@parser_classes([JSONParser, MultiPartParser ])
@permission_classes((CurriculumApiAccessPolicy,))
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
def curriculumApi(request, curriculum_id=0):

    if request.method == "GET":
        if curriculum_id == 0:
            query_object = CurriculumApiAccessPolicy.scope_query_object(request=request)
            curriculums = Curriculum.objects.filter(query_object).order_by('id')

            if not curriculums.exists():
                return JsonResponse("The objects do not exist.", safe=False)

            curriculum_serializer = CurriculumSerializer(curriculums, many=True, context={'request': request})
            return JsonResponse(curriculum_serializer.data, safe=False)

        else:
            query_object = CurriculumApiAccessPolicy.scope_query_object(request=request)
            curriculum = Curriculum.objects.filter(Q(id=curriculum_id) & query_object).first()

            if curriculum is None:
                return JsonResponse("The object does not exist.", safe=False)

            curriculum_serializer = CurriculumSerializer(event, context={'request': request})
            return JsonResponse(curriculum_serializer.data, safe=False)

    elif request.method == "POST":
        curriculum_data = request.data.dict()
        curriculum_data = CurriculumSerializer.custom_clean(data=curriculum_data, context={'request': request})
        curriculum_serializer = CurriculumSerializer(data=curriculum_data, context={'request': request})

        if curriculum_serializer.is_valid():
            success = True
            try:
                with transaction.atomic():
                    curriculum_serializer.save()
            except IntegrityError:
                success = False
            if success:
                return JsonResponse("Added Successfully", safe=False)
            else:
                return JsonResponse("Failed to add.", safe=False)

        else:
            print(curriculum_serializer.error_messages)
            print(curriculum_serializer.errors)
            return JsonResponse("Failed to Add", safe=False)

    elif request.method == "PUT":
        query_object = CurriculumApiAccessPolicy.scope_query_object(request=request)
        curriculum = Curriculum.objects.filter(Q(id=curriculum_id) & query_object).first()

        if curriculum is None:
            return JsonResponse("Failed to update.", safe=False)

        curriculum_data = request.data.dict()
        curriculum_data = CurriculumSerializer.custom_clean(instance=curriculum, data=curriculum_data, context={'request': request})
        curriculum_serializer = CurriculumSerializer(curriculum, data=curriculum_data, context={'request': request})

        if curriculum_serializer.is_valid():
            success = True
            try:
                with transaction.atomic():
                    curriculum_serializer.save()
            except IntegrityError:
                success = False
            if success:
                return JsonResponse("Updated Successfully", safe=False)
            else:
                return JsonResponse("Failed to delete.", safe=False)

        else:
            print(curriculum_serializer.errors)
            print(curriculum_serializer.error_messages)
            return JsonResponse("Failed to Update")


    elif request.method == "DELETE":
        query_object = CurriculumApiAccessPolicy.scope_query_object(request=request)
        curriculum = Curriculum.objects.filter(Q(id=curriculum_id) & query_object).first()

        if curriculum is None:
            return JsonResponse("Failed to delete.", safe=False)

        success = True
        try:
            with transaction.atomic():
                curriculum.delete()
        except IntegrityError:
            success = False
        if success:
            return JsonResponse("Deleted Successfully", safe=False)
        else:
            return JsonResponse("Failed to delete.", safe=False)


def skillgroup(request):
    return render(request, 'profile/skillgroup.html', {})

@parser_classes([JSONParser, MultiPartParser])
@permission_classes((SkillGroupApiAccessPolicy,))
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
def skillGroupApi(request, skillgroup_id=0):

    Serializer = SkillGroupSerializer
    AccessPolicyClass = SkillGroupApiAccessPolicy
    Model = Skillgroup

    if request.method == "GET":
        if skillgroup_id == 0:
            query_object = AccessPolicyClass.scope_query_object(request=request)
            objects = Model.objects.filter(query_object).order_by('id')

            if not objects.exists():
                return JsonResponse("The objects do not exist.", safe=False)

            serializer = Serializer(objects, many=True, context={'request': request})
            print(serializer.data)
            return JsonResponse(serializer.data, safe=False)
        else:
            id = skillgroup_id
            query_object = AccessPolicyClass.scope_query_object(request=request)
            object = Model.objects.filter(Q(id=id) & query_object).first()

            if object is None:
                return JsonResponse("The object does not exist.", safe=False)

            serializer = Serializer(object, context={'request': request})
            print(serializer.data)
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
        id = skillgroup_id
        query_object = AccessPolicyClass.scope_query_object(request=request)
        object = Model.objects.filter(Q(id=id) & query_object).first()

        if object is None:
            return JsonResponse("Failed to update.", safe=False)

        data = request.data.dict()
        # print(data)
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

    elif request.method == "DELETE":
        id = skillgroup_id
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







#Testing AccessPolicy

# @permission_classes((EventAccessPolicy,))
# @authentication_classes((SessionAuthentication, BasicAuthentication))
# @api_view(("GET",))
# @permission_classes((EventAccessPolicy,))
# def eventWithAccessPolicyApi(request, eventId=0):
#
#     if request.method=='GET':
#         event = Event.objects.get(eventId=eventId)
#         event_serializer = EventAccessPolicyTestSerializer(event, context = {'request':request})
#         print(event_serializer.data)
#         return JsonResponse(event_serializer.data, safe=False)
#
# @permission_classes((EventAccessPolicy,))
# @api_view(("GET",))
# @authentication_classes((SessionAuthentication, BasicAuthentication))
# def listEventsWithAccessPolicyApi(request):
#     if request.method =='GET':
#         events = Event.objects.filter(approved__in=[True])
#         events_serializer = EventAccessPolicyTestSerializer(events, many=True, context = {'request':request})
#         return JsonResponse(events_serializer.data, safe=False)
