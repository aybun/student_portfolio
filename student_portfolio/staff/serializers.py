from rest_framework import serializers
from .models import Staff

class StaffSerializer(serializers.ModelSerializer):


    userId = serializers.IntegerField(required=False)
    staffId = serializers.CharField(min_length=11, max_length=11, required=False, allow_blank=True)

    firstname = serializers.CharField(max_length=50, required=False, allow_blank=True)
    middlename = serializers.CharField(max_length=50, required=False, allow_blank=True)
    lastname = serializers.CharField(max_length=50, required=False, allow_blank=True)

    class Meta:
        model = Staff
        fields = ('userId', 'staffId', 'firstname', 'middlename', 'lastname')
