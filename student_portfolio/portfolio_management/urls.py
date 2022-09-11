from django.urls import re_path, path
from . import views

urlpatterns=[

    path('home', views.home),
    path('logoutpage', views.logoutView ),

    path('api/user', views.userApi),

]