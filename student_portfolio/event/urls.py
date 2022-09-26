from django.urls import re_path, path
from rest_framework import routers
from . import views

urlpatterns=[
    # re_path(r'^event$', views.eventApi),
    # re_path(r'^event/([0-9]+)$', views.eventApi),
    # path('event', views.eventApi),


    # re_path(r'^event/view/([0-9]+)$', views.xxxxxxxxxxx),


    #SYNC
    path('api/syncStudentAttendanceByStudentId/<int:eventId>', views.syncStudentAttendanceByStudentId),

    #Using Django template
    path('event', views.event),
    path('api/event', views.eventApi),
    path('api/event/<int:eventId>', views.eventApi),

    path('event/eventRegisterRequest', views.eventRegisterRequest),
    path('api/eventRegisterRequest', views.eventRegisterRequestApi),
    path('api/eventRegisterRequest/<int:eventId>', views.eventRegisterRequestApi),

    path('eventAttendanceOfStudents/<int:eventId>', views.eventAttendanceOfStudents),
    path('api/eventAttendanceOfStudents/', views.eventAttendanceOfStudentsApi),
    path('api/eventAttendanceOfStudents/<int:eventId>', views.eventAttendanceOfStudentsApi),
    path('api/eventAttendanceOfStudents/<int:eventId>/<str:studentId>', views.eventAttendanceOfStudentsApi),

    path('api/skillTable', views.skillTableApi),

    #Test Access policy
    path('api/testEvent/<int:eventId>', views.eventWithAccessPolicyApi),
    path('api/testListEvents', views.listEventsWithAccessPolicyApi),

]

# router = routers.SimpleRouter()
# router.register(r'api/testEvent/<int:eventId>')