from rest_framework import serializers
import json
from django.contrib.auth.models import User

from event.serializers import EventSerializer
from .models import Project
from event.models import Skill

from rest_access_policy import FieldAccessMixin, AccessPolicy
from .access_policies import ProjectApiAccessPolicy

class ProjectSkillSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)

    class Meta:
        model = Skill
        fields = ('id',)

class ProjectStaffSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)

    class Meta:
        model = User
        fields = ('id',)

class ProjectSerializer(FieldAccessMixin, serializers.ModelSerializer):

    id = serializers.IntegerField(required=False, read_only=True)

    title = serializers.CharField(max_length=100, required=True)
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)

    info = serializers.CharField(max_length=200, allow_blank=True)

    created_by = serializers.PrimaryKeyRelatedField(many=False, read_only=False, allow_null=True, required=False, queryset=User.objects.all())

    approved = serializers.BooleanField(required=False)
    approved_by = serializers.PrimaryKeyRelatedField(many=False, read_only=False, allow_null=True, required=False, queryset=User.objects.all())
    used_for_calculation = serializers.BooleanField(required=False)

    attachment_link = serializers.URLField(required=False, max_length=200, allow_blank=True)
    attachment_file = serializers.FileField(required=False, allow_null=True)

    skills = ProjectSkillSerializer(many=True, read_only=False, allow_null=True, required=False)
    staffs = ProjectStaffSerializer(many=True, read_only=False, allow_null=True, required=False)

    class Meta:
        model = Project
        fields = '__all__'

        access_policy = ProjectApiAccessPolicy

    def update(self, instance, validated_data):

        instance.title = validated_data.get('title', instance.title)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.info = validated_data.get('info', instance.info)
        instance.created_by = validated_data.get('created_by', instance.created_by)
        instance.approved = validated_data.get('approved', instance.approved)
        instance.approved_by = validated_data.get('approved_by', instance.approved_by)
        instance.used_for_calculation = validated_data.get('used_for_calculation', instance.used_for_calculation)
        instance.attachment_link = validated_data.get('attachment_link', instance.attachment_link)
        instance.attachment_file = validated_data.get('attachment_file', instance.attachment_file)

        # Update many-to-many relationships
        instance.skills.clear()
        if 'skills' in validated_data:
            for e in validated_data.get('skills'):
                instance.skills.add(Skill.objects.get(id=e['id']))

        instance.staffs.clear()
        if 'staffs' in validated_data:
            for e in validated_data.get('staffs'):
                instance.staffs.add(User.objects.get(id=e['id']))

        instance.save()
        return instance


    @staticmethod
    def custom_clean(instance=None, data=None, context=None ):

        request = context['request']
        method = request.method
        groups = request.user.groups.values_list('name', flat=True)

        #Clean data

        if method == 'POST':

            data['created_by'] = request.user.id

        elif method == 'PUT':

            attachment_file = data.get('attachment_file', None)
            if isinstance(attachment_file, str):
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
                if instance.approved: #If the project has already been approved. We won't reassign this user to approved_by.
                    data.pop('approved')
                else:
                    if data['approved'] == 'true':
                        data['approved_by'] = request.user.id
                    else:
                        data.pop('approved_by', None)

        return data
