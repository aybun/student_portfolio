from django.urls import re_path
from . import views

urlpatterns=[
    re_path(r'^student$', views.studentApi),
    re_path(r'^student/([0-9]+)$', views.studentApi),

    # re_path(r'^student$', views.authStudentApiView.as_view()),
    # re_path(r'^student/([0-9]+)$', views.authStudentApiView.as_view()),

    # re_path(r'^employee/savefile',views.SaveFile)

]