from django.db import models

from student.models import Student
from staff.models import Staff

# from djongo import models
from django import forms

# Create your models here.

class Event(models.Model):
    eventId = models.BigAutoField(primary_key=True)

    title = models.CharField(max_length=100)
    date = models.DateField()

    mainStaffId = models.CharField(max_length=11)

    info = models.CharField(max_length=200)


class EventAttendanceOfStudents(models.Model):

    eventId = models.BigIntegerField()
    studentId = models.CharField(max_length=11)

    #student
    firstname = models.CharField(max_length=50, blank=True)
    middlename = models.CharField(max_length=50, blank=True)
    lastname = models.CharField(max_length=50, blank=True)

    synced = models.BooleanField(default=False)

