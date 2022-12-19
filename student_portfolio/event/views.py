# import django.db.transaction
from django.shortcuts import render
from django.db import IntegrityError, transaction
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.db.models import Q

from student.models import Student
from .models import Event, StudentAttendEvent, Skill
from .serializers import EventSerializer, SkillSerializer, EventAccessPolicyTestSerializer, EventAccessPolicy, \
    EventSkillSerializer, StudentAttendEventSerializer

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

                if events is None:
                    return JsonResponse({}, safe=False)

                event_serializer=EventSerializer(events, many=True, context={'request': request})
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
                event_serializer.save()
                return JsonResponse("Added Successfully", safe=False)

                # success = True
                # try:
                #     with transaction.atomic():
                #         event_serializer.save()
                # except IntegrityError:
                #
                #     success = False
                #
                # if success:
                #     return JsonResponse("Added Successfully", safe=False)
                # else:
                #     return JsonResponse("Failed to add.", safe=False)

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
            print(data)
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

        event = Event.objects.filter(id=event_id).first()


        if event is None:
            return JsonResponse("Failed to delete.", safe=False)

        # print('student' in groups and (event.created_by == request.user.id) and (not event.approved))
        if 'staff' in groups or \
                ('student' in groups and (event.created_by.id == request.user.id) and (not event.approved)):

            success = True
            try:
                with transaction.atomic():

                    Event.objects.filter(id=event_id).delete()

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
@permission_classes((StudentAttendEventApiAccessPolicy,))
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
def eventAttendanceOfStudentsApi(request, event_id=0, attendance_id=0):

    groups = list(request.user.groups.values_list('name', flat=True))

    if request.method=='GET':
        if 'staff' in groups:
            if (attendance_id == 0):

                query_object = StudentAttendEventApiAccessPolicy.scope_query_object(request=request)
                attendances = StudentAttendEvent.objects.filter( Q(event_id_fk=event_id) & query_object ).order_by('id')
                serializer = StudentAttendEventSerializer(attendances, many=True, context={'request' : request})

                return JsonResponse(serializer.data, safe=False)
            else:
                query_object = StudentAttendEventApiAccessPolicy.scope_query_object(request=request)
                attendance = StudentAttendEvent.objects.filter(Q(id=attendance_id) & query_object).first()

                if attendance is None:
                    return JsonResponse("The object does not exist.", safe=False)

                serializer = StudentAttendEventSerializer(attendance, context={'request' : request})
                return JsonResponse(serializer.data, safe=False)


        elif 'student' in groups:
            student = Student.objects.get(user_id_fk=request.user.id)
            attendances = StudentAttendEvent.objects.filter(student_id_fk=student.id)

            if not attendances.exists():
                return JsonResponse("The objects do not exist.", safe=False)

            event_id_list = attendances.values_list('event_id_fk', flat=True)

            events = Event.objects.filter(id__in=event_id_list)

            if events.exists():
                event_serializer = EventSerializer(events, many=True, context={'request': request})
                return JsonResponse(event_serializer.data, safe=False)
            else:
                return JsonResponse("The objects do not exist.", safe=False)

        # elif 'student' in groups:
        #
        #     if (eventId == 0): #Get all events this student joined.
        #         student = Student.objects.get(userId=request.user.id)
        #         attendances = EventAttendanceOfStudents.objects.filter(studentId=student.studentId)
        #         serializer = EventAttendanceOfStudentsSerializer(attendances, many=True)
        #         return JsonResponse(serializer.data, safe=False)


    elif request.method=='POST':
        if 'staff' in groups:

            attendance_data = request.data.dict()
            print(attendance_data)
            attendance = StudentAttendEvent.objects.filter(event_id_fk=attendance_data['event_id_fk'],
                                                           student_id=attendance_data['student_id'])

            if not attendance.exists():
                serializer = StudentAttendEventSerializer(data=attendance_data, context={'request' : request})
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

            attendance_data = StudentAttendEventSerializer.custom_clean(data=attendance_data, context={'request' : request})

            print(attendance_data)
            attendance = StudentAttendEvent.objects.filter(id=attendance_data['id']).first()
            if attendance is None:
                return JsonResponse("Failed to Update", safe=False)

            serializer=StudentAttendEventSerializer(attendance, data=attendance_data, context={'request' : request})

            if serializer.is_valid():
                serializer.save()
                return JsonResponse("Updated Successfully",safe=False)
            else:
                print(serializer.error_messages)
                print(serializer.errors)
                return JsonResponse("Failed to Update", safe=False)

    elif request.method=='DELETE': #Need to handle carefully.

        if 'staff' in groups:
            attendance = StudentAttendEvent.objects.get(id=attendance_id)

            if attendance is not None:
                attendance.delete()
                return JsonResponse("Deleted Successfully", safe=False)
            else:
                return JsonResponse("Object not found", safe=False)


@csrf_exempt
def syncStudentAttendanceByStudentId(request, event_id=0):

    if request.method == 'PUT':

        #Make queries.
        attendances = StudentAttendEvent.objects.filter(event_id_fk=event_id)
        student_id_of_attendees_list = attendances.values_list('student_id', flat=True)
        first_two_letters_set = set([e[:2] for e in student_id_of_attendees_list])
        query_string = Q()
        for e in first_two_letters_set:
            query_string = query_string | Q(student_id__startswith=e)

        students = Student.objects.filter(query_string).values_list('student_id', 'id')
        print(students)
        student_ids = [e[0] for e in students]
        student_id_fks = [e[1] for e in students]
        print(student_ids)
        print(student_id_fks)
        #Delete Duplications.
        to_be_saved = []
        unique_student_ids = []
        for attendance in attendances:
            if attendance.student_id not in unique_student_ids:
                unique_student_ids.append(attendance.student_id)
                to_be_saved.append(attendance)
            else:
                attendance.delete()

        #Set synced=True and Set student_id_fk.
        attendances = to_be_saved
        for attendance in attendances:
            for i in range(0, len(student_ids)):
                if attendance.student_id == student_ids[i]:
                    attendance.synced = True
                    attendance.student_id_fk = Student.objects.get(id=student_id_fks[i])

                    # print(attendance)
                    # print(attendance.)

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
