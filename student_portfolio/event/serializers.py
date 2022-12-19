from rest_framework import serializers

from staff.models import Staff
from student.models import Student
from .models import Event, StudentAttendEvent, Skill
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User


from rest_access_policy import FieldAccessMixin, AccessPolicy
from .access_policies import EventApiAccessPolicy, StudentAttendEventApiAccessPolicy

from datetime import datetime
import json

class SkillSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    title = serializers.CharField(max_length=50, required=True)
    goal_point = serializers.IntegerField(min_value=0, max_value=10,  required=False)

    # events = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all(), many=True)

    class Meta:
        model = Skill
        fields = ('id', 'title', 'goal_point')

class EventSkillSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)

    class Meta:
        model = Skill
        fields = ('id',)

class EventStaffSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)

    class Meta:
        model = Staff
        fields = ('id',)

class EventSerializer(FieldAccessMixin, serializers.ModelSerializer):

    id = serializers.IntegerField(required=False, read_only=True)
    title = serializers.CharField(max_length=100, required=True)
    start_datetime = serializers.DateTimeField(required=False, format="%Y-%m-%dT%H:%M")
    end_datetime = serializers.DateTimeField(required=False, format="%Y-%m-%dT%H:%M")

    info = serializers.CharField(max_length=200, allow_blank=True)

    created_by = serializers.PrimaryKeyRelatedField(many=False, read_only=False, allow_null=True, required=False, queryset=User.objects.all())
    approved = serializers.BooleanField(required=False)
    approved_by = serializers.PrimaryKeyRelatedField(many=False, read_only=False, allow_null=True, required=False, queryset=User.objects.all())

    used_for_calculation = serializers.BooleanField(required=False)
    arranged_inside = serializers.BooleanField(required=False)

    attachment_link = serializers.URLField(required=False, max_length=200, allow_blank=True)

    attachment_file = serializers.FileField(required=False, allow_null=True)

    skills = EventSkillSerializer(many=True, read_only=False, allow_null=True, required=False)
    staffs = EventStaffSerializer(many=True, read_only=False, allow_null=True, required=False)

    class Meta:
        model = Event
        fields = ('id', 'title', 'start_datetime', 'end_datetime', 'info', 'created_by',
                  'approved', 'approved_by', 'used_for_calculation', 'arranged_inside', 'attachment_link',
                  'attachment_file', 'skills', 'staffs')

        access_policy = EventApiAccessPolicy


    def update(self, instance, validated_data):

        instance.title = validated_data.get('title', instance.title)
        instance.start_datetime = validated_data.get('start_datetime', instance.start_datetime)
        instance.end_datetime = validated_data.get('end_datetime', instance.end_datetime)
        instance.info = validated_data.get('info', instance.info)
        instance.created_by = validated_data.get('created_by', instance.created_by)
        instance.approved = validated_data.get('approved', instance.approved)
        instance.approved_by = validated_data.get('approved_by', instance.approved_by)
        instance.used_for_calculation = validated_data.get('used_for_calculation', instance.used_for_calculation)
        instance.arranged_inside = validated_data.get('arranged_inside', instance.arranged_inside)
        instance.attachment_link = validated_data.get('attachment_link', instance.attachment_link)
        instance.attachment_file = validated_data.get('attachment_file', instance.attachment_file)

        #Update many-to-many relationships
        instance.skills.clear()
        if 'skills' in validated_data:
            for e in validated_data.get('skills'):
                instance.skills.add(Skill.objects.get(id=e['id']))

        instance.staffs.clear()
        if 'staffs' in validated_data:
            for e in validated_data.get('staffs'):
                instance.staffs.add(Staff.objects.get(id=e['id']))

        instance.save()
        return instance


    @staticmethod
    def custom_clean_skills(instance=None, data=None, context=None):

        #Assume that data is a stringnified object.
        skill_ids = Skill.objects.all().values_list('id', flat=True)

        list_of_dicts = json.loads(data)

        if not(isinstance(list_of_dicts, list)) or len(list_of_dicts) == 0: # If it is not a list, return an empty string ''. So that we could pop this field.
            return ''

        #Do We really need this???
        unique_ids = []
        out_list = []
        for e in list_of_dicts:

            id = e['id']
            if id not in skill_ids:
                raise serializers.ValidationError(
                    "The skillId is not present in the Skill table : " + str(e['id']))

            if id not in unique_ids:
                unique_ids.append(id)
                out_list.append(e)

        return out_list

    @staticmethod
    def custom_clean_staffs(instance=None, data=None, context=None):
        # staff_id_fks = Staff.objects.all().values_list('id', flat=True)
        #Need to check for correctness and redundancies.
        list_of_dicts = json.loads(data)

        if not (isinstance(list_of_dicts, list)) or len(
                list_of_dicts) == 0:  # If it is not a list, return an empty string ''. So that we could pop this field.
            return ''

        return list_of_dicts


    @staticmethod
    def custom_clean(instance=None, data=None, context=None):
        # print(data)
        request = context['request']
        method = request.method
        groups = request.user.groups.values_list('name', flat=True)


        if method == 'POST':
            data['created_by'] = request.user.id

        elif method == 'PUT':

            if isinstance(data.get('attachment_file', None), str):
                data.pop('attachment_file', None)

            if 'skills' in data:
                data['skills'] = EventSerializer.custom_clean_skills(data=data['skills']) #If it contains errors, the function will return a string, might be ''.
                if isinstance(data.get('skills', None), str):
                    data.pop('skills', None)

            if 'staffs' in data:
                data['staffs'] = EventSerializer.custom_clean_staffs(data=data['staffs'])
                if isinstance(data.get('staffs', None), str):
                    data.pop('staffs', None)

            if 'staff' in groups:
                if data['approved'] == 'true':
                    data['approved_by'] = request.user.id
                else:
                    data.pop('approved_by', None)

        return data


class StudentAttendEventSerializer(FieldAccessMixin, serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    event_id_fk = serializers.PrimaryKeyRelatedField(many=False, read_only=False, allow_null=True, required=True, queryset=Event.objects.all())

    student_id = serializers.CharField(min_length=11, max_length=11, required=True)

    firstname = serializers.CharField(max_length=50, required=False, allow_blank=True)
    middlename = serializers.CharField(max_length=50, required=False, allow_blank=True)
    lastname = serializers.CharField(max_length=50, required=False, allow_blank=True)

    student_id_fk = serializers.PrimaryKeyRelatedField(many=False, read_only=False, allow_null=True, required=False, queryset=Student.objects.all())

    synced = serializers.BooleanField(required=False)
    used_for_calculation = serializers.BooleanField( required=False)

    class Meta:
        model = StudentAttendEvent
        fields = ('id', 'event_id_fk', 'student_id', 'firstname', 'middlename', 'lastname', 'student_id_fk', 'synced', 'used_for_calculation')

        access_policy = StudentAttendEventApiAccessPolicy

    @staticmethod
    def custom_clean(instance=None, data=None, context=None):
        request = context['request']
        groups = request.user.groups.values_list('name', flat=True)


        if request.method == "PUT":

            student_id_fk = data['student_id_fk']
            if student_id_fk == '' or student_id_fk == 'null':
                data.pop('student_id_fk', None)

        return data


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

