from django.urls import re_path, path
from . import views

urlpatterns=[

    path('home', views.home),
    path('logoutpage', views.logoutView ),

    path('api/user', views.userApi),

    path('files/<str:file_id>', views.file),

    path('api/files/<str:file_id>', views.fileApi),
]