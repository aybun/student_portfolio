from rest_access_policy import FieldAccessMixin
from rest_framework import serializers

from .access_policies import UserProfileApiAccessPolicy, StaffApiAccessPolicy, StudentApiAccessPolicy
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

    class Meta:
        model = UserProfile
        fields = ('id', 'university_id', 'user_id_fk', 'firstname', 'middlename', 'lastname', 'faculty_role')

        access_policy = StudentApiAccessPolicy

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