from django.urls import re_path, path
# from rest_framework import routers
from . import views

urlpatterns=[
    # re_path(r'^event$', views.eventApi),
    # re_path(r'^event/([0-9]+)$', views.eventApi),
    # path('event', views.eventApi),


    # re_path(r'^event/view/([0-9]+)$', views.xxxxxxxxxxx),




    #Using Django template
    path('event', views.event),
    path('api/event', views.eventApi),
    path('api/event/<int:event_id>', views.eventApi),

    # path('event/eventRegisterRequest', views.eventRegisterRequest),
    # path('api/eventRegisterRequest', views.eventRegisterRequestApi),
    # path('api/eventRegisterRequest/<int:event_id>', views.eventRegisterRequestApi),

    path('eventAttendanceOfStudents/<int:event_id>', views.eventAttendanceOfStudents),
    path('api/eventAttendanceOfStudents/', views.eventAttendanceOfStudentsApi),
    path('api/eventAttendanceOfStudents/<int:event_id>', views.eventAttendanceOfStudentsApi),
    path('api/eventAttendanceOfStudents/<int:event_id>/<int:attendance_id>', views.eventAttendanceOfStudentsApi),
#SYNC
    path('api/syncStudentAttendanceByStudentId/<int:event_id>', views.syncStudentAttendanceByStudentId),


    path('api/skillTable', views.skillTableApi),

    #Test Access policy
    path('api/testEvent/<int:eventId>', views.eventWithAccessPolicyApi),
    path('api/testListEvents', views.listEventsWithAccessPolicyApi),

]

# router = routers.SimpleRouter()
# router.register(r'api/testEvent/<int:eventId>')