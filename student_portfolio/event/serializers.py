from rest_framework import serializers
from .models import Event, EventAttendanceOfStudents, Skill
from rest_framework.parsers import JSONParser
import json

from rest_access_policy import FieldAccessMixin, AccessPolicy


class EventModelFieldAccessPolicy(AccessPolicy):
    statements = []

    @classmethod
    def scope_fields(cls, request, fields: dict, instance=None) -> dict:
        groups = request.user.groups.values_list('name', flat=True)

        #Field Access
        if 'staff' not in groups:
            fields.pop('approved', None)
            fields.pop('used_for_calculation', None)

        #Cleaning data
        if request.method == "POST":
            #We force users to create the event first.
            fields.pop('attachment_link', None)
            fields.pop('attachment_file', None)

        # elif request.method == "PUT":
        #     # attachment_link = fields.get('attachment_link')
        #     # attachment_file = fields.get('attachment_file')
        #
        #     atm_link = fields.get('attachment_file')
        #     atm_file = fields.get('attachment_file')
        #
        #     print('{} {}'.format('attachment_link', atm_link.value))
        #     print('{} {}'.format('attachment_file', atm_file.value))
        #
        #
        #     if atm_link == '':
        #         fields.pop('attachment_link')
        #
        #     if atm_file == '' or atm_file == 'null':
        #         fields.pop('attachment_file')

        return fields

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

        access_policy = EventModelFieldAccessPolicy

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
    def custom_clean(data):
        attachment_file = data.get('attachment_file', None)
        attachment_link = data.get('attachment_link', None)

        if attachment_file == '' or attachment_file == 'null':
            data.pop('attachment_file', None)
        if attachment_link == '':
            data.pop('attachment_file', None)

        return data

    # def validate_attachment_file(self, input):
    #
    #     if input == '':
    #         return None
    #
    # def validate_attachment_link(self, input):
    #     if input == '':
    #         return None

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
    # skillId = serializers.IntegerField(required=False)
    title = serializers.CharField(max_length=50, required=True)

    class Meta:
        model = Skill
        fields = ('skillId', 'title')



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