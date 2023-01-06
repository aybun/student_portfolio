from django.urls import path

from . import views

urlpatterns=[
    
    path('profile/', views.info),
    path('profile/info', views.info),
    path('profile/charts', views.charts),
    path('profile/edit-student-profile', views.editStudentProfile),

    path('api/staff', views.staffApi),
    path('api/staff/<int:userprofile_id>', views.staffApi),

    path('api/student', views.studentApi),
    path('api/student/<int:userprofile_id>', views.studentApi),

    path('api/profile', views.profileApi),
    path('api/profile/<int:userprofile_id>', views.profileApi),


]
