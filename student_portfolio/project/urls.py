from django.urls import re_path, path
# from rest_framework import routers
from . import views


urlpatterns = [

    path('project/<int:projectId>', views.project),
    path('api/projectApi/<int:projectId>', views.projectApi),

]