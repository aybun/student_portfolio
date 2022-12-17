# import django.db.transaction
from django.shortcuts import render
from django.db import IntegrityError, transaction
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.db.models import Q

from student.models import Student
from .models import Event, StudentAttendEvent, Skill
from .serializers import EventSerializer, SkillSerializer, EventAccessPolicyTestSerializer, EventAccessPolicy, \
    EventSkillSerializer

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
                # events = Event.objects.filter(approved__in=[True])
                events = Event.objects.all()

                if events is None:
                    return JsonResponse({}, safe=False)

                event_serializer=EventSerializer(events, many=True, context={'request': request})
                # print(event_serializer.data)
                return JsonResponse(event_serializer.data, safe=False)
            else:
                #Note : Add staff.

                event = Event.objects.get(id=event_id)
                event_serializer = EventSerializer(event, context={'request' : request})
                # print(event_serializer.data)

                # event_skills = EventSkill.objects.filter(event_id_fk=event_id)
                # event_skill_serializer = EventSkillSerializer(event_skills, many=True)
                #
                # out_data = event_serializer.data
                # out_data['skills'] = event_skill_serializer.data
                # print(event_serializer.data)
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
            print(event_data)
            event_serializer = EventSerializer(data=event_data, context={'request':request})

            if event_serializer.is_valid():
                event_serializer.save(created_by=request.user)
                return JsonResponse("Added Successfully", safe=False)
            else:
                print(event_serializer.error_messages)
                print(event_serializer.errors)
                return JsonResponse("Failed to Add", safe=False)

    elif request.method=='PUT':

        event = Event.objects.get(id=event_id)
        if event is None:
            return JsonResponse("Failed to update.", safe=False)

        if 'staff' in groups or ('student' in groups and event.created_by == request.user.id and (not event.approved)):
            #Note : Update Staff.

            data = request.data.dict()
            # print(data)
            event_data = EventSerializer.custom_clean(instance=event, data=data, context={'request' : request})
            print(event_data)
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

        event = Event.objects.get(id=event_id)

        if event is None:
            return JsonResponse("Failed to delete.", safe=False)

        if 'staff' in groups or \
                ('student' in groups and (event.created_by == request.user.id) and (not event.approved)):

            success = True
            try:
                with transaction.atomic():
                    # attendances = EventAttendanceOfStudents.objects.filter(id=event_id)
                    # attendances_delete_report = attendances.delete()

                    Event.objects.filter(id=event_id).delete()
                    # event_delete_report = event.delete()

            except IntegrityError:
                success=False

            if success:
                return JsonResponse("Deleted Successfully", safe=False)
            else:
                return JsonResponse("Failed to delete.", safe=False)

def eventAttendanceOfStudents(request, eventId=0, studentId='0'):

    groups = list(request.user.groups.values_list('name', flat=True))

    if 'staff' in groups:
        if studentId == '0': #get all students joined the event.
            stuff_for_frontend = { 'eventId' : eventId }
            return render(request, 'event/event_attendance_of_students.html', stuff_for_frontend)
    else:
        return render(request, 'home/error.html', {'error_message': 'The user has no permission to access.'})

# @csrf_exempt
# def eventAttendanceOfStudentsApi(request, eventId=0, studentId='0'):
#
#     groups = list(request.user.groups.values_list('name', flat=True))
#
#     if request.method=='GET':
#         if 'staff' in groups:
#             if (studentId == '0'):
#                 # print('This path. ' + studentId )
#                 attendances = EventAttendanceOfStudents.objects.filter(eventId__exact=eventId)
#                 serializer = EventAttendanceOfStudentsSerializer(attendances, many=True)
#                 return JsonResponse(serializer.data, safe=False)
#             else:
#                 # print('This path.')
#                 attendance = EventAttendanceOfStudents.objects.filter(eventId__exact=eventId, studentId__exact=studentId)
#                 serializer = EventAttendanceOfStudentsSerializer(attendance)
#                 return JsonResponse(serializer.data, safe=False)
#
#         elif 'student' in groups:
#
#             if (eventId == 0): #Get all events this student joined.
#                 student = Student.objects.get(userId=request.user.id)
#                 attendances = EventAttendanceOfStudents.objects.filter(studentId=student.studentId)
#                 serializer = EventAttendanceOfStudentsSerializer(attendances, many=True)
#                 return JsonResponse(serializer.data, safe=False)
#
#
#     elif request.method=='POST':
#         attendance_data=JSONParser().parse(request)
#         # print(attendance_data)
#         attendance = EventAttendanceOfStudents.objects.filter(studentId=attendance_data['studentId'])
#
#         if attendance is None:
#             serializer=EventAttendanceOfStudentsSerializer(data=attendance_data)
#         else:
#             return JsonResponse("Failed to Add", safe=False)
#
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse("Added Successfully",safe=False)
#         else:
#             print(serializer.error_messages)
#             print(serializer.errors)
#             return JsonResponse("Failed to Add",safe=False)
#
#     elif request.method=='PUT':
#         attendance_data=JSONParser().parse(request)
#         print(attendance_data)
#
#         attendance=EventAttendanceOfStudents.objects.get(eventId__exact=eventId,
#                                                          studentId__exact=studentId)
#
#         attendance_data['studentId'] = attendance_data['newStudentId']
#         serializer=EventAttendanceOfStudentsSerializer(attendance, data=attendance_data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse("Updated Successfully",safe=False)
#         else:
#             print(serializer.error_messages)
#             print(serializer.errors)
#             return JsonResponse("Failed to Update", safe=False)
#
#     elif request.method=='DELETE': #Need to handle carefully.
#
#         attendance = EventAttendanceOfStudents.objects.get(eventId=eventId, studentId=studentId)
#         # print(attendance)
#         if attendance is not None:
#             attendance.delete()
#             return JsonResponse("Deleted Successfully", safe=False)
#         else:
#             return JsonResponse("Object not found", safe=False)


@csrf_exempt
def syncStudentAttendanceByStudentId(request, eventId=0):

    if request.method == 'PUT':
        # data = JSONParser().parse(request)
        # eventId = data['eventId']

        event = Event.objects.get(eventId__exact=eventId)
        attendances = EventAttendanceOfStudents.objects.filter(eventId__exact=eventId).order_by('studentId')

        studentIdsAttended = attendances.values_list('studentId', flat=True)
        id_set_1 = set(studentIdsAttended) #List of Ids stored in EventAttendanceOfStudents.

        studentsAttended = Student.objects.filter(studentId__in=studentIdsAttended).order_by('studentId')
        id_set_2 = set(studentsAttended.values_list('studentId', flat=True))

        syncable_id_set = id_set_1.intersection(id_set_2) # can be safely synced.

        syncables = attendances.filter(studentId__in=syncable_id_set).order_by('studentId')
        # print(syncables[0])
        # print(syncables[0].eventId)

        if (attendances is not None) and (event is not None):

            for i in range(0, len(syncables)):
                syncables[i].firstname  = studentsAttended[i].firstname
                syncables[i].middlename = studentsAttended[i].middlename
                syncables[i].lastname   = studentsAttended[i].lastname

                syncables[i].synced = True
                syncables[i].save()

            return JsonResponse("Synced successfully", safe=False)

        return JsonResponse("Failed to sync", safe=False)


@parser_classes([JSONParser, MultiPartParser ])
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


@csrf_exempt
def eventRegisterRequest(request):

    if not request.user.is_authenticated:
        return render(request, 'home/error.html', {'error_message': 'The user has no permission to access.'})

    stuff_for_frontend = {}

    return render(request, 'event/event_register_request.html', stuff_for_frontend)

@csrf_exempt
def eventRegisterRequestApi(request, eventId=0):

    groups = request.user.groups.values_list('name', flat=True)

    if request.method == 'GET':
        # if not request.user.is_authenticated:
        #     return JsonResponse("Permission denied.", safe=False)

        if 'staff' in groups:

            events = Event.objects.filter(approved__in=[False])
            serializer = EventSerializer(events, many=True, context={'request' : request})
            return JsonResponse(serializer.data, safe=False)

        elif 'student' in groups:
            # The issue of djongo : https://stackoverflow.com/questions/68609027/djongo-fails-to-query-booleanfield

            events = Event.objects.filter(created_by=request.user.id, approved__in=[False])
            serializer = EventSerializer(events, many=True, context={'request' : request})
            # print('{} : {}'.format('data', serializer.data ))
            return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':

        event_data = JSONParser().parse(request)
        event_data['created_by'] = request.user.id

        events_serializer = EventSerializer(data=event_data, context={'request' : request})

        if events_serializer.is_valid():
            events_serializer.save()
            return JsonResponse("Added Successfully", safe=False)

        return JsonResponse("Failed to Add", safe=False)

    if request.method == 'PUT':

        if 'staff' in groups:
            event_data = JSONParser().parse(request)
            event = Event.objects.get(eventId=eventId)

            if not event:
                return JsonResponse("The object does not exist.")

            # event_data.pop('hello', None)
            serializer = EventSerializer(event, data=event_data, context={'request' : request})
            if serializer.is_valid():
                serializer.save()
                return JsonResponse("Updated Successfully", safe=False)
            else:
                print(serializer.errors)
                print(serializer.error_messages)
                return JsonResponse("Failed to Update", safe=False)

        elif 'student' in groups:

            data = JSONParser().parse(request)
            event_data = data['event']
            # Pop fields that are not allowed to be altered by non-staff. We might outright reject such request.
            # event_data.pop('approved', None)
            # event_data.pop('used_for_calculation', None)

            event = Event.objects.get(eventId=eventId, created_by=request.user.id)

            if not event:
                return JsonResponse("The object does not exist.", safe=False)

            serializer = EventSerializer(event, data=event_data, context={'request' : request})

            if serializer.is_valid():
                serializer.save()
                return JsonResponse("Updated Successfully", safe=False)
            else:
                print(serializer.errors)
                print(serializer.error_messages)
                return JsonResponse("Failed to Update", safe=False)

    if request.method == 'DELETE':
        pass


#Testing AccessPolicy

# @permission_classes((EventAccessPolicy,))
# @authentication_classes((SessionAuthentication, BasicAuthentication))
@api_view(("GET",))
@permission_classes((EventAccessPolicy,))
def eventWithAccessPolicyApi(request, eventId=0):

    if request.method=='GET':
        event = Event.objects.get(eventId=eventId)
        event_serializer = EventAccessPolicyTestSerializer(event, context = {'request':request})
        print(event_serializer.data)
        return JsonResponse(event_serializer.data, safe=False)

@permission_classes((EventAccessPolicy,))
@api_view(("GET",))
@authentication_classes((SessionAuthentication, BasicAuthentication))
def listEventsWithAccessPolicyApi(request):
    if request.method =='GET':
        events = Event.objects.filter(approved__in=[True])
        events_serializer = EventAccessPolicyTestSerializer(events, many=True, context = {'request':request})
        return JsonResponse(events_serializer.data, safe=False)
