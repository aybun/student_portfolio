from django.urls import re_path
from . import views

urlpatterns=[
    re_path(r'^staff$', views.staffApi),
    re_path(r'^staff/([0-9]+)$', views.staffApi),

    # re_path(r'^employee/savefile',views.SaveFile)

]