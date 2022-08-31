from django.urls import re_path, path

from . import views

urlpatterns=[
    # re_path(r'^event$', views.eventApi),
    # re_path(r'^event/([0-9]+)$', views.eventApi),
    path('event', views.eventApi),
    path('event/<int:id>/', views.eventApi),

    # re_path(r'^event/view/([0-9]+)$', views.xxxxxxxxxxx),

    path('eventAttendanceOfStudents/<int:eventId>', views.eventAttendanceOfStudentsApi),
    path('eventAttendanceOfStudents/<int:eventId>/<str:studentId>', views.eventAttendanceOfStudentsApi),

    #SYNC
    path('syncStudentAttendanceByStudentId/<int:eventId>', views.syncStudentAttendanceByStudentId),

]