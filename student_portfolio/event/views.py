from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from .models import Event, EventAttendanceOfStudents
from .serializers import EventSerializer, EventAttendanceOfStudentsSerializer

from student.models import Student
from django.core.files.storage import default_storage

# Create your views here.
def event(request, id=0):

    if not request.user.is_authenticated:
        pass

    if id == 0: #want all events

        # events = Event.objects.all()
        # # print(events)
        # events_serializer = EventSerializer(events, many=True)
        # dict_data = events_serializer.data
        # print(dict_data)

        return render(request, 'event/event.html', {'is_staff' : request.user.is_staff})

    # if not request.user.is_staff: #The user is student.
    #     student = Student.objects.get(userId__exact=request.user.id)
    #     event_joined = EventAttendanceOfStudents.objects.filter(studentId=student.studentId)
    #     event_serializer = EventAttendanceOfStudentsSerializer(event_joined, many=True)
    #
    #     dict_data = event_serializer.data[0]
    #     dict_data['is_staff'] = False
    #
    #     return render(request, 'event/event.html', dict_data)

    if request.user.is_staff:
        pass


@csrf_exempt
def eventApi(request, id=0):
    if request.method=='GET':
        if (id == 0):

            events = Event.objects.all()
            events_serializer=EventSerializer(events, many=True)
            return JsonResponse(events_serializer.data, safe=False)
        else:
            event = Event.objects.get(eventId=id)
            event_serializer = EventSerializer(event)
            return JsonResponse(event_serializer.data, safe=False)

    elif request.method=='POST':

        if not request.user.is_staff:
            return JsonResponse("You do not have permission add new item.", safe=False)

        event_data=JSONParser().parse(request)

        events_serializer=EventSerializer(data=event_data)

        if events_serializer.is_valid():
            events_serializer.save()
            return JsonResponse("Added Successfully",safe=False)
        return JsonResponse("Failed to Add",safe=False)

    elif request.method=='PUT':

        if not request.user.is_staff:
            return JsonResponse("You do not have permission to edit the item.", safe=False)


        event_data=JSONParser().parse(request)
        event=Event.objects.get(eventId=event_data['eventId'])
        serializer = EventSerializer(event, data=event_data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update")

    elif request.method=='DELETE': #Need to handle carefully.
        if not request.user.is_staff:
            return JsonResponse("You do not have permission to delete the item.", safe=False)


        attendances = EventAttendanceOfStudents.objects.filter(eventId__exact=id)
        attendances.delete()

        event=Event.objects.get(eventId=id)
        event.delete()
        return JsonResponse("Deleted Successfully",safe=False)

def eventAttendanceOfStudents(request, eventId=0, studentId='0'):

    if request.user.is_staff:
        if studentId == '0': #get all students joined the event.
            stuff_for_frontend = { 'eventId' : eventId}
            return render(request, 'event/event_attendance_of_students.html', stuff_for_frontend)
    else:
        return render(request, 'home/error.html', {'error_message': 'The user has no permission to access.'})


@csrf_exempt
def eventAttendanceOfStudentsApi(request, eventId=0, studentId='0'):
    # print(eventId)
    # print(studentId)
    if request.method=='GET':

        if (studentId == '0'):
            # print('This path. ' + studentId )
            attendances = EventAttendanceOfStudents.objects.filter(eventId__exact=eventId)
            serializer = EventAttendanceOfStudentsSerializer(attendances, many=True)
            return JsonResponse(serializer.data, safe=False)
        else:
            # print('This path.')
            attendance = EventAttendanceOfStudents.objects.filter(eventId__exact=eventId, studentId__exact=studentId)
            serializer = EventAttendanceOfStudentsSerializer(attendance)
            return JsonResponse(serializer.data, safe=False)

    elif request.method=='POST':
        attendance_data=JSONParser().parse(request)
        print(attendance_data)
        serializer=EventAttendanceOfStudentsSerializer(data=attendance_data)
        # print(serializer.is_valid())
        if serializer.is_valid():
            serializer.save()
            return JsonResponse("Added Successfully",safe=False)
        else:
            print(serializer.error_messages)
            print(serializer.errors)

        return JsonResponse("Failed to Add",safe=False)

    elif request.method=='PUT':
        attendance_data=JSONParser().parse(request)
        print(attendance_data)

        attendance=EventAttendanceOfStudents.objects.get(eventId__exact=eventId,
                                                         studentId__exact=studentId)

        attendance_data['studentId'] = attendance_data['newStudentId']
        serializer=EventAttendanceOfStudentsSerializer(attendance, data=attendance_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse("Updated Successfully",safe=False)
        else:
            print(serializer.error_messages)
            print(serializer.errors)

        return JsonResponse("Failed to Update", safe=False)

    elif request.method=='DELETE': #Need to handle carefully.

        attendance = EventAttendanceOfStudents.objects.get(eventId=eventId, studentId=studentId)
        print(attendance)
        if attendance is not None:
            attendance.delete()
            return JsonResponse("Deleted Successfully", safe=False)
        else:
            return JsonResponse("Object not found", safe=False)



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
