from django.contrib.auth.models import User
from rest_access_policy import FieldAccessMixin
from rest_framework import serializers

from .access_policies import PrivateModelAccessPolicy
from .models import PrivateModel

class PrivateModelSerializer(FieldAccessMixin, serializers.ModelSerializer ):
    id = serializers.IntegerField(required=True)
    private_file_1 = serializers.FileField(required=False, allow_null=True)
    private_file_2 = serializers.FileField(required=False, allow_null=True)

    created_by = serializers.PrimaryKeyRelatedField(many=False, read_only=False, allow_null=True, required=False,
                                                    queryset=User.objects.all())

    class Meta:
        model = PrivateModel
        fields = ('id', 'private_file_1', 'private_file_2', 'created_by')
        access_policy = PrivateModelAccessPolicy


    def update(self, instance, validated_data):

        instance.private_file_1 = validated_data.get('private_file_1', instance.private_file_1)
        instance.private_file_2 = validated_data.get('private_file_2', instance.private_file_2)
        instance.created_by = validated_data.get('created_by', instance.created_by)
        instance.save()

        return instance

    @staticmethod
    def custom_clean(instance=None, data=None, context=None):
        # print(data)
        request = context['request']
        method = request.method
        groups = request.user.groups.values_list('name', flat=True)

        if method == 'POST':
            data['created_by'] = request.user.id
        if method == 'PUT':

            if isinstance(data.get('private_file_1', None), str):
                data.pop('private_file_1', None)

            if isinstance(data.get('private_file_2', None), str):
                data.pop('private_file_2', None)


        return data

