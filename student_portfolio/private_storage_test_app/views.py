from django.db import transaction, IntegrityError
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import parser_classes, api_view, permission_classes, authentication_classes
from rest_framework.parsers import JSONParser, MultiPartParser

from private_storage_test_app.access_policies import PrivateModelAccessPolicy
from private_storage_test_app.models import PrivateModel
from private_storage_test_app.serializers import PrivateModelSerializer
from student_portfolio.settings import PRIVATE_STORAGE_ROOT

# Create your views here.
from private_storage.views import PrivateStorageView
from private_storage.storage.files import PrivateFileSystemStorage

storage = PrivateFileSystemStorage(
    location=PRIVATE_STORAGE_ROOT,
    base_url='/private-media/'
)

class StorageView(PrivateStorageView):
    storage = storage

    def can_access_file(self, private_file):
        # This overrides PRIVATE_STORAGE_AUTH_FUNCTION
        filename = private_file.filename

        return self.request.is_superuser

def testprivate(request, id=0):

    # if not request.user.is_authenticated:
    #     return render(request, 'home/error.html', {'error_message': 'The user has no permission to access.'})

    return render(request, 'testprivate/testprivate.html', {})

@parser_classes([JSONParser, MultiPartParser ])
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes((PrivateModelAccessPolicy,))
@authentication_classes((SessionAuthentication, BasicAuthentication))
def testprivateApi(request, project_id=0):

    Serializer = PrivateModelSerializer
    AccessPolicyClass = PrivateModelAccessPolicy
    Model = PrivateModel

    if request.method == "GET":
        if project_id == 0:
            query_object = AccessPolicyClass.scope_query_object(request=request)
            objects = Model.objects.filter(query_object).order_by('id')

            if not objects.exists():
                return JsonResponse("The objects do not exist.", safe=False)

            serializer = Serializer(objects, many=True, context={'request': request})
            print(serializer.data)
            return JsonResponse(serializer.data, safe=False)
        else:
            id = project_id
            query_object = AccessPolicyClass.scope_query_object(request=request)
            object = Model.objects.filter(Q(id=id) & query_object).first()

            if object is None:
                return JsonResponse("The object does not exist.", safe=False)

            serializer = Serializer(object, context={'request': request})
            return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = request.data.dict()
        data = Serializer.custom_clean(data=data, context={'request': request})
        serializer = Serializer(data=data, context={'request': request})

        if serializer.is_valid():
            success = True
            try:
                with transaction.atomic():
                    serializer.save()
            except IntegrityError:
                success = False

            if success:
                return JsonResponse("Added Successfully", safe=False)
            else:
                return JsonResponse("Failed to add.", safe=False)

        else:
            print(serializer.error_messages)
            print(serializer.errors)
            return JsonResponse("Failed to Add", safe=False)

    elif request.method == "PUT":
        id = project_id
        print('id : {}'.format(id))
        query_object = AccessPolicyClass.scope_query_object(request=request)
        object = Model.objects.filter(Q(id=id) & query_object).first()

        if object is None:
            return JsonResponse("Failed to update.", safe=False)

        data = request.data.dict()
        print(data)
        data = Serializer.custom_clean(instance=object, data=data, context={'request': request})
        serializer = Serializer(object, data=data, context={'request': request})


        if serializer.is_valid():
            success = True
            try:
                with transaction.atomic():
                    serializer.save()
            except IntegrityError:
                success = False
            if success:
                return JsonResponse("Updated Successfully", safe=False)
            else:
                return JsonResponse("Failed to delete.", safe=False)

        else:
            print(serializer.errors)
            print(serializer.error_messages)
            return JsonResponse("Failed to Update")

    elif request.method == "DELETE":
        id = project_id
        query_object = AccessPolicyClass.scope_query_object(request=request)
        object = Model.objects.filter(Q(id=id) & query_object).first()

        if object is None:
            return JsonResponse("Failed to delete.", safe=False)

        success = True
        try:
            with transaction.atomic():
                object.delete()
        except IntegrityError:
            success = False
        if success:
            return JsonResponse("Deleted Successfully", safe=False)
        else:
            return JsonResponse("Failed to delete.", safe=False)