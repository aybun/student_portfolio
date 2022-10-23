from rest_framework import serializers
from .models import Event, EventAttendanceOfStudents, Skill
from rest_framework.parsers import JSONParser
import json

from rest_access_policy import FieldAccessMixin, AccessPolicy
from .access_policies import EventApiAccessPolicy

class EventSerializer(FieldAccessMixin, serializers.ModelSerializer):

    eventId = serializers.IntegerField(required=False, read_only=True)
    title = serializers.CharField(max_length=100, required=True)
    date = serializers.DateField(required=True)

    mainStaffId = serializers.CharField(max_length=11, allow_blank=True)

    info = serializers.CharField(max_length=200, allow_blank=True)
    skills = serializers.JSONField(default=[])

    created_by = serializers.IntegerField(required=False)

    approved = serializers.BooleanField(required=False)
    used_for_calculation = serializers.BooleanField(required=False)

    attachment_link = serializers.URLField(required=False, max_length=200, allow_blank=True)
    # Validate attachment_file
    attachment_file = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = Event
        fields = ('eventId', 'title', 'date', 'mainStaffId', 'info', 'skills', 'created_by',
                  'approved', 'used_for_calculation', 'attachment_link', 'attachment_file')

        access_policy = EventApiAccessPolicy

    def validate_skills(self, stringnified_list_of_dicts):
        skill_ids = Skill.objects.all().values_list('skillId', flat=True)

        list_of_dicts = json.loads(stringnified_list_of_dicts)

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

    @staticmethod
    def custom_clean(instance=None, data=None, context=None):

        request = context['request']
        method = request.method
        groups = request.user.groups.values_list('name', flat=True)


        attachment_file = data.get('attachment_file', None)
        attachment_link = data.get('attachment_link', None)
        if attachment_file == '' or attachment_file == 'null':
            data.pop('attachment_file', None)

        if attachment_link == '':
            data.pop('attachment_link', None)

        if method == 'POST':
            data['created_by'] = request.user.id
        elif method == 'PUT':

            if 'student' in groups:
                if instance.approved: #Do not update if the event is already approved.
                    data = {}



        return data

    # def create(self, validated_data):
    #     return self.Meta.model.objects.create(**validated_data)


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
    skillId = serializers.IntegerField(required=False)
    title = serializers.CharField(max_length=50, required=True)

    goal_point = serializers.IntegerField(min_value=0, max_value=10,  required=False)
    type = serializers.IntegerField(required=False)
    class Meta:
        model = Skill
        fields = ('skillId', 'title', 'goal_point', 'type')



class EventAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["eventWithAccessPolicyApi"],
            "principal": ["group:gods", "group:laymen"],
            "effect": "allow"
        },
        {
            "action": ["listEventsWithAccessPolicyApi"],
            "principal": ["group:gods"],
            "effect": "allow"
        }
    ]

    @classmethod
    def scope_fields(cls, request, fields: dict, instance=None) -> dict:

        groups = request.user.groups.values_list('name', flat=True)
        print(groups)
        if 'staff' not in groups:
            fields.pop('created_by', None)

        return fields



class EventAccessPolicyTestSerializer(FieldAccessMixin, serializers.ModelSerializer):

    eventId = serializers.IntegerField(required=False, read_only=True)
    title = serializers.CharField(max_length=100, required=True)
    date = serializers.DateField(required=True)

    mainStaffId = serializers.CharField(max_length=11, allow_blank=True)

    info = serializers.CharField(max_length=200, allow_blank=True)
    skills = serializers.JSONField(default=[])

    created_by = serializers.IntegerField(required=False)

    approved = serializers.BooleanField(required=False)
    used_for_calculation = serializers.BooleanField(required=False)

    attachment_link = serializers.URLField(required=False, max_length=200, allow_blank=True)
    # Validate attachment_file
    attachment_file = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = Event
        fields = ('eventId', 'title', 'date', 'mainStaffId', 'info', 'skills', 'created_by',
                  'approved', 'used_for_calculation', 'attachment_link', 'attachment_file')

        access_policy = EventAccessPolicy

    def validate_skills(self, stringnified_list_of_dicts):
        skill_ids = Skill.objects.all().values_list('skillId', flat=True)

        list_of_dicts = json.loads(stringnified_list_of_dicts)

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

    def validate_attachment_file(self, input):

        return input

