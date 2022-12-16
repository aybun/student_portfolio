from rest_framework import serializers
from .models import Event, StudentAttendEvent, Skill
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User


from rest_access_policy import FieldAccessMixin, AccessPolicy
from .access_policies import EventApiAccessPolicy

from datetime import datetime
import json

class EventSerializer(FieldAccessMixin, serializers.ModelSerializer):

    id = serializers.IntegerField(required=False, read_only=True)
    title = serializers.CharField(max_length=100, required=True)
    start_datetime = serializers.DateTimeField(required=False, format="%Y-%m-%dT%H:%M")
    end_datetime = serializers.DateTimeField(required=False, format="%Y-%m-%dT%H:%M")

    info = serializers.CharField(max_length=200, allow_blank=True)

    created_by = serializers.PrimaryKeyRelatedField(many=False, read_only=False, allow_null=True, queryset=User.objects.all())
    approved = serializers.BooleanField(required=False)
    approved_by = serializers.PrimaryKeyRelatedField(required=False, read_only=False, allow_null=True, queryset=User.objects.all())

    used_for_calculation = serializers.BooleanField(required=False)
    arranged_inside = serializers.BooleanField(required=False)

    attachment_link = serializers.URLField(required=False, max_length=200, allow_blank=True)

    attachment_file = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = Event
        fields = ('id', 'title', 'start_datetime', 'end_datetime', 'info', 'created_by',
                  'approved', 'approved_by', 'used_for_calculation', 'arranged_inside', 'attachment_link',
                  'attachment_file')

        access_policy = EventApiAccessPolicy

    # def validate_skills(self, stringnified_list_of_dicts):
    #     skill_ids = Skill.objects.all().values_list('skillId', flat=True)
    #
    #     list_of_dicts = json.loads(stringnified_list_of_dicts)
    #
    #     unique_ids = []
    #     out_list = []
    #     for e in list_of_dicts:
    #
    #         id = e['skillId']
    #         if id not in skill_ids:
    #             raise serializers.ValidationError("The skillId is not present in the Skill table : " + str(e['skillId']) )
    #
    #         if id not in unique_ids:
    #             unique_ids.append(id)
    #             out_list.append(e)
    #
    #     return out_list

    @staticmethod
    def custom_clean(instance=None, data=None, context=None):
        print(data)
        request = context['request']
        method = request.method
        groups = request.user.groups.values_list('name', flat=True)


        attachment_file = data.get('attachment_file', None)
        attachment_link = data.get('attachment_link', None)
        if isinstance(attachment_file, str):
            data.pop('attachment_file', None)

        if attachment_link == '':
            data.pop('attachment_link', None)

        if method == 'POST':
            pass
            # data['created_by'] = request.user.id
        elif method == 'PUT':
            pass
            # if 'staff' in groups:
            #     if data['approved']:
            #         data['approved_by'] = request.user.id

        return data

    def validate_created_by(self, value):
        print('hello from created_by')
        if isinstance(value, User):
            return value.id

        return value

    def validate_approved_by(self, value):
        if isinstance(value, User):
            return value.id

        return value

    # def update(self, instance, validated_data):
    #     fields = ('id', 'title', 'start_datetime', 'end_datetime', 'info', 'created_by',
    #               'approved', 'approved_by', 'used_for_calculation', 'arranged_inside', 'attachment_link',
    #               'attachment_file')
    #
    #     instance.title = validated_data['']

    # def create(self, validated_data):
    #     return self.Meta.model.objects.create(**validated_data)


# class EventAttendanceOfStudentsSerializer(serializers.ModelSerializer):
#     eventId = serializers.IntegerField(required=True)
#     studentId = serializers.CharField(min_length=11, max_length=11, required=True)
#
#     firstname = serializers.CharField(max_length=50, required=False, allow_blank=True)
#     middlename = serializers.CharField(max_length=50, required=False, allow_blank=True)
#     lastname = serializers.CharField(max_length=50, required=False, allow_blank=True)
#
#     synced = serializers.BooleanField(default=False, required=False)
#
#     class Meta:
#         model = EventAttendanceOfStudents
#         fields = ('eventId', 'studentId', 'firstname', 'middlename', 'lastname', 'synced')
#         # fields = '__all__'


class SkillSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    title = serializers.CharField(max_length=50, required=True)
    goal_point = serializers.IntegerField(min_value=0, max_value=10,  required=False)

    class Meta:
        model = Skill
        fields = ('id', 'title', 'goal_point')

class EventSkillSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    skill_id_fk = serializers.IntegerField(required=False)
    event_id_fk = serializers.IntegerField(required=False)

    class Meta:
        model = Skill
        fields = '__all__'

    # @staticmethod
    # def custom_clean(instance=None, data=None, context=None):
    #
    #     request = context['request']
    #     method = request.method
    #     groups = request.user.groups.values_list('name', flat=True)
    #
    #     # data = list of skill_ids.
    #     event_id = request.data['id']
    #
    #     list_of_pairs = [] #(skill_id, event_id)
    #     for skill_id in data:
    #         list_of_pairs.append((skill_id))




class EventAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["eventWithAccessPolicyApi"],
            "principal": ["group:student", "group:staff"],
            "effect": "allow"
        },
        {
            "action": ["eventWithAccessPolicyApi"],
            "principal": ["group:student"],
            "effect": "deny"
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

