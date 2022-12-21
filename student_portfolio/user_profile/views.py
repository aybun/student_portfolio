from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from .models import UserProfile
from .serializers import UserProfileSerializer
# Create your views here.


def info(request):

    return render(request, 'profile/info.html', {})


def charts(request):

    return render(request, 'profile/charts.html', {})


def staffApi(request, id=0):

    if request.method=='GET':
        staffs = UserProfile.objects.filter(faculty_role__id=1) #staff
        staff_serializer = UserProfileSerializer(staffs, many=True)

        return JsonResponse(staff_serializer.data, safe=False)
    # elif request.method == 'POST':
    #     staff_data = JSONParser().parse(request)
    #     staff_serializer=StaffSerializer(data=staff_data)
    #
    #     if staff_serializer.is_valid():
    #         staff_serializer.save()
    #         return JsonResponse("Added Successfully", safe=False)
    #     return JsonResponse("Failed to Add", safe=False)
    #
    # elif request.method == 'PUT':
    #     staff_data = JSONParser().parse(request)
    #     staff = Staff.objects.get(id=staff_data['id'])
    #     staff_serializer = StaffSerializer(staff, data=staff_data)
    #
    #     if staff_serializer.is_valid():
    #         staff_serializer.save()
    #         return JsonResponse("Updated Successfully", safe=False)
    #
    #     return JsonResponse("Failed to Update")
    #
    # elif request.method == 'DELETE':
    #     staff=Staff.objects.get(id=id)
    #     staff.delete()
    #     return JsonResponse("Deleted Successfully", safe=False)