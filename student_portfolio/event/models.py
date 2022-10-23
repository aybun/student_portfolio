from django.db import models
# from djongo import models
from django.conf import settings

from student.models import Student
from staff.models import Staff

# from djongo import models
from django import forms

# Create your models here.

class Skill(models.Model):
    skillId = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=50)

    goal_point = models.BigIntegerField(default=0)
    type = models.IntegerField(default=0)
    # detail = models.CharField(max_length=100)

    def __str__(self):
        return self.title


def event_attachment_file_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'events/{0}/{1}'.format(instance.eventId, filename)

class Event(models.Model):
    eventId = models.BigAutoField(primary_key=True)

    title = models.CharField(max_length=100)
    date = models.DateField(null=True, blank=False)

    mainStaffId = models.CharField(max_length=11, blank=True, default='')

    info = models.CharField(max_length=200, blank=True, default='')

    skills = models.JSONField(default=dict)

    #user_id
    created_by = models.BigIntegerField(null=False, editable=False)

    approved = models.BooleanField(default=False)
    used_for_calculation = models.BooleanField(default=False)

    attachment_link = models.URLField(max_length=200, blank=True, default='')
    attachment_file = models.FileField(upload_to=event_attachment_file_directory_path, null=True, blank=True)


class EventAttendanceOfStudents(models.Model):

    eventId = models.BigIntegerField()
    studentId = models.CharField(max_length=11)

    #student
    firstname = models.CharField(max_length=50, blank=True)
    middlename = models.CharField(max_length=50, blank=True)
    lastname = models.CharField(max_length=50, blank=True)

    synced = models.BooleanField(default=False)


