from django.urls import path

from . import views

urlpatterns=[
    
    path('profile/', views.info),
    path('profile/info', views.info),
    path('profile/charts', views.charts),

    path('api/staff', views.staffApi),
    path('api/staff/<int:id>', views.staffApi),
]
