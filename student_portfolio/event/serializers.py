from rest_framework import serializers
from .models import Event, EventAttendanceOfStudents

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class EventAttendanceOfStudentsSerializer(serializers.ModelSerializer):
    eventId = serializers.IntegerField(required=True)
    studentId = serializers.CharField(min_length=11, max_length=11, required=True)

    firstname = serializers.CharField(max_length=50, required=False, allow_blank=True)
    middlename = serializers.CharField(max_length=50, required=False, allow_blank=True)
    lastname = serializers.CharField(max_length=50, required=False, allow_blank=True)

    synced = serializers.BooleanField(default=False, required=False)

    class Meta:
        model = EventAttendanceOfStudents
        # fields = ('eventId', 'studentId')
        fields = '__all__'


