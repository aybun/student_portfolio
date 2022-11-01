from rest_framework import serializers
import json

from .models import Project
from event.models import Skill

from rest_access_policy import FieldAccessMixin, AccessPolicy
from .access_policies import ProjectApiAccessPolicy



class ProjectSerializer(FieldAccessMixin, serializers.ModelSerializer):

    projectId = serializers.IntegerField(required=False, read_only=True)

    title = serializers.CharField(max_length=100, required=True)
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)

    # consider adding more staffs.
    mainStaffId = serializers.CharField(max_length=11, allow_blank=True)
    info = serializers.CharField(max_length=200, allow_blank=True)

    skills = serializers.JSONField(default=[])

    # user_id
    proposed_by = serializers.IntegerField(required=False)

    approved = serializers.BooleanField(required=False)
    approved_by = serializers.IntegerField(required=False)
    used_for_calculation = serializers.BooleanField(required=False)

    attachment_link = serializers.URLField(required=False, max_length=200, allow_blank=True)
    attachment_file = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = Project
        fields = '__all__'

        access_policy = ProjectApiAccessPolicy

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
    def custom_clean(instance=None, data=None, context=None ):

        request = context['request']
        method = request.method
        groups = request.user.groups.values_list('name', flat=True)

        #Clean data
        attachment_file = data.get('attachment_file', None)
        if isinstance(attachment_file, str):
            data.pop('attachment_file', None)

        attachment_link = data.get('attachment_link', None)
        if attachment_link == '':
            data.pop('attachment_link', None)

        if method == 'POST':

            data['proposed_by'] = request.user.id

        elif method == 'PUT':
            if 'staff' in groups:
                if instance.approved: #If the project has already been approved. We won't reassign this user to approved_by.
                    data.pop('approved')
                else:
                    if data['approved']:
                        data['approved_by'] = request.user.id

        return data
