from rest_framework import serializers
from .models import Event, EventAttendanceOfStudents, Skill

class EventSerializer(serializers.ModelSerializer):

    eventId = serializers.IntegerField(required=False, read_only=True)
    title = serializers.CharField(max_length=100, required=True)
    date = serializers.DateField(required=True)

    mainStaffId = serializers.CharField(max_length=11, allow_blank=True)

    info = serializers.CharField(max_length=200, allow_blank=True)
    skills = serializers.JSONField(default=[])

    created_by = serializers.IntegerField(required=False)

    approved = serializers.BooleanField(required=False)
    used_for_calculation = serializers.BooleanField(required=False)

    class Meta:
        model = Event
        fields = ('eventId', 'title', 'date', 'mainStaffId', 'info', 'skills', 'created_by', 'approved', 'used_for_calculation')

    def validate_skills(self, list_of_dicts):
        skill_ids = Skill.objects.all().values_list('skillId', flat=True)

        unique_ids = []
        out_list = []
        for e in list_of_dicts:

            id = e['skillId']
            if id not in skill_ids:
                raise serializers.ValidationError("The skillId is not present in the Skill table : " + str(e['skillId']) )

            if id not in unique_ids:
                unique_ids.append(id)
                out_list.append(e)

        return out_list



class EventAttendanceOfStudentsSerializer(serializers.ModelSerializer):
    eventId = serializers.IntegerField(required=True)
    studentId = serializers.CharField(min_length=11, max_length=11, required=True)

    firstname = serializers.CharField(max_length=50, required=False, allow_blank=True)
    middlename = serializers.CharField(max_length=50, required=False, allow_blank=True)
    lastname = serializers.CharField(max_length=50, required=False, allow_blank=True)

    synced = serializers.BooleanField(default=False, required=False)

    class Meta:
        model = EventAttendanceOfStudents
        fields = ('eventId', 'studentId', 'firstname', 'middlename', 'lastname', 'synced')
        # fields = '__all__'


class SkillSerializer(serializers.ModelSerializer):
    # skillId = serializers.IntegerField(required=True)
    title = serializers.CharField(max_length=50, required=True)

    class Meta:
        model = Skill
        fields = ('skillId', 'title')
