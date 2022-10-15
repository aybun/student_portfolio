from django.urls import re_path, path
from . import views


urlpatterns = [

    path('project/', views.project),
    # path('project/<int:projectId>', views.project),
    path('api/project', views.projectApi),
    path('api/project/<int:projectId>', views.projectApi),

]