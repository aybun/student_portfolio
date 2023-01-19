from rest_access_policy import FieldAccessMixin
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from event.models import Curriculum
from .access_policies import UserProfileApiAccessPolicy, StaffApiAccessPolicy, StudentApiAccessPolicy, \
    CurriculumStudentBulkAddApiAccessPolicy
from .models import UserProfile, FacultyRole
from django.contrib.auth.models import User


class StaffSerializer(FieldAccessMixin, serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    university_id = serializers.CharField(min_length=11, max_length=11, required=False, allow_blank=True)
    user_id_fk = serializers.PrimaryKeyRelatedField(many=False, read_only=False, allow_null=True, queryset=User.objects.all())

    firstname = serializers.CharField(max_length=50, required=False, allow_blank=True)
    middlename = serializers.CharField(max_length=50, required=False, allow_blank=True)
    lastname = serializers.CharField(max_length=50, required=False, allow_blank=True)

    faculty_role = serializers.PrimaryKeyRelatedField(many=False, read_only=False,
                                                      allow_null=True, required=False, queryset=FacultyRole.objects.all())

    class Meta:
        model = UserProfile
        fields = ('id', 'university_id', 'user_id_fk', 'firstname', 'middlename', 'lastname', 'faculty_role')

        access_policy = StaffApiAccessPolicy

class StudentSerializer(FieldAccessMixin, serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    university_id = serializers.CharField(min_length=11, max_length=11, required=False, allow_blank=True)
    user_id_fk = serializers.PrimaryKeyRelatedField(many=False, read_only=False, allow_null=True, queryset=User.objects.all())

    firstname = serializers.CharField(max_length=50, required=False, allow_blank=True)
    middlename = serializers.CharField(max_length=50, required=False, allow_blank=True)
    lastname = serializers.CharField(max_length=50, required=False, allow_blank=True)

    faculty_role = serializers.PrimaryKeyRelatedField(many=False, read_only=False,
                                                      allow_null=True, required=False, queryset=FacultyRole.objects.all())

    enroll = serializers.PrimaryKeyRelatedField(many=False, read_only=False, allow_null=True, queryset=Curriculum.objects.all())

    class Meta:
        model = UserProfile
        fields = ('id', 'university_id', 'user_id_fk', 'firstname', 'middlename', 'lastname', 'faculty_role', 'enroll')

        access_policy = StudentApiAccessPolicy

    def update(self, instance, validated_data):

        instance.enroll = validated_data.get('enroll', instance.enroll)
        instance.save()

        return instance

    @staticmethod
    def custom_clean(instance=None, data=None, context=None):
        request = context['request']
        groups = request.user.groups.values_list('name', flat=True)


        if request.method == "PUT":
            pass


        return data

class CurriculumStudentBulkAddSerializer(FieldAccessMixin, serializers.Serializer):
    curriculum_id = serializers.IntegerField(required=True)
    csv_file = serializers.FileField(required=True, allow_empty_file=False)

    class Meta:
        # Model = EventAttendance
        fields = ('event_id', 'csv_file')
        access_policy = CurriculumStudentBulkAddApiAccessPolicy

    def validate_curriculum_id(self, event_id):
        instance = Curriculum.objects.filter(id=event_id)

        if not instance.exists():
            raise ValidationError("The curriculum_id = {} does not exist.".format(event_id))

        return event_id

    def validate_csv_file(self, file):
        if file.size > 10000000:
            raise ValidationError("The file size must be less than 10 mb.")

        return file





class UserProfileSerializer(FieldAccessMixin, serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    university_id = serializers.CharField(min_length=11, max_length=11, required=False, allow_blank=True)
    user_id_fk = serializers.PrimaryKeyRelatedField(many=False, read_only=False, allow_null=True, queryset=User.objects.all())

    firstname = serializers.CharField(max_length=50, required=False, allow_blank=True)
    middlename = serializers.CharField(max_length=50, required=False, allow_blank=True)
    lastname = serializers.CharField(max_length=50, required=False, allow_blank=True)

    faculty_role = serializers.PrimaryKeyRelatedField(many=False, read_only=False,
                                                      allow_null=True, required=False, queryset=FacultyRole.objects.all())

    class Meta:
        model = UserProfile
        fields = ('id', 'university_id', 'user_id_fk', 'firstname', 'middlename', 'lastname', 'faculty_role')

        access_policy = UserProfileApiAccessPolicy