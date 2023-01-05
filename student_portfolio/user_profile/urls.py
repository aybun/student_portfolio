from django.urls import path

from . import views

urlpatterns=[
    
    path('profile/', views.info),
    path('profile/info', views.info),
    path('profile/charts', views.charts),

    path('api/staff', views.staffApi),
    path('api/staff/<int:id>', views.staffApi),

    path('api/profile', views.profileApi),
    path('api/profile/<int:userprofile_id>', views.profileApi),


]
