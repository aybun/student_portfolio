from django.urls import re_path, path

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
    path('api/event/<int:id>', views.eventApi),

    path('eventAttendanceOfStudents/<int:eventId>', views.eventAttendanceOfStudents),
    path('api/eventAttendanceOfStudents/<int:eventId>', views.eventAttendanceOfStudentsApi),
    path('api/eventAttendanceOfStudents/<int:eventId>/<str:studentId>', views.eventAttendanceOfStudentsApi),

    path('api/skillTable', views.skillTableApi),
]