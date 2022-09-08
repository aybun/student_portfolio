from django.db import models
# from djongo import models

from student.models import Student
from staff.models import Staff

# from djongo import models
from django import forms

# Create your models here.

class Skill(models.Model):
    skillId = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=50)
    # detail = models.CharField(max_length=100)

    def __str__(self):
        return self.title



class Event(models.Model):
    eventId = models.BigAutoField(primary_key=True)

    title = models.CharField(max_length=100)
    date = models.DateField(null=True, blank=False)

    mainStaffId = models.CharField(max_length=11, blank=True, default='')

    info = models.CharField(max_length=200, blank=True, default='')

    skills = models.JSONField(default=dict)

    #user_id
    created_by = models.BigIntegerField(null=False)

    approved = models.BooleanField(default=False)
    used_for_calculation = models.BooleanField(default=False)


class EventAttendanceOfStudents(models.Model):

    eventId = models.BigIntegerField()
    studentId = models.CharField(max_length=11)

    #student
    firstname = models.CharField(max_length=50, blank=True)
    middlename = models.CharField(max_length=50, blank=True)
    lastname = models.CharField(max_length=50, blank=True)

    synced = models.BooleanField(default=False)


