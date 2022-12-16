from django.db import models
# from djongo import models
from django.conf import settings
from django.contrib.auth.models import User

from student.models import Student
from staff.models import Staff

# from djongo import models
from django import forms

# Create your models here.


def event_attachment_file_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'events/{0}/{1}'.format(instance.id, filename)


class Event(models.Model):
    id = models.BigAutoField(primary_key=True)

    title = models.CharField(max_length=100)
    start_datetime = models.DateTimeField(null=True, blank=False)
    end_datetime = models.DateTimeField(null=True, blank=False)

    # mainStaffId = models.CharField(max_length=11, blank=True, default='')

    info = models.CharField(max_length=200, blank=True, default='')

    # skills = models.JSONField(default=dict)

    #user_id
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='event_created_by_set')
    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='event_approved_by_set')

    used_for_calculation = models.BooleanField(default=False)
    arranged_inside = models.BooleanField(default=False)

    attachment_link = models.URLField(max_length=200, blank=True, default='')
    attachment_file = models.FileField(upload_to=event_attachment_file_directory_path, null=True, blank=True)

#should we let it record staff?????
class StudentAttendEvent(models.Model):
    id = models.BigAutoField(primary_key=True)

    event_id_fk = models.ForeignKey(Event, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=11)

    #student
    firstname = models.CharField(max_length=50, blank=True, default='')
    middlename = models.CharField(max_length=50, blank=True, default='')
    lastname = models.CharField(max_length=50, blank=True, default='')

    user_id_fk = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    synced = models.BooleanField(default=False)
    used_for_calculation = models.BooleanField(default=False)


class StaffManageEvent(models.Model):
    id = models.BigAutoField(primary_key=True)

    event_id_fk = models.ForeignKey(Event, on_delete=models.CASCADE)
    user_id_fk = models.ForeignKey(User, on_delete=models.CASCADE)
    is_main_staff = models.BooleanField(default=False)


class Skill(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=50)

    goal_point = models.BigIntegerField(default=0)
    # info = models.CharField(max_length=200, default='')
    # detail = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class EventSkill(models.Model):
    id = models.BigAutoField(primary_key=True)
    skill_id_fk = models.ForeignKey(Skill, on_delete=models.CASCADE)
    event_id_fk = models.ForeignKey(Event, on_delete=models.CASCADE)


class SkillGroup(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=50)
    info = models.CharField(max_length=200, default='')


class AssignSkillToSkillGroup(models.Model):
    id = models.BigAutoField(primary_key=True)
    skill_id_fk = models.ForeignKey(Skill, on_delete=models.CASCADE)
    skill_group_id_fk = models.ForeignKey(SkillGroup, on_delete=models.CASCADE)


def curriculum_attachment_file_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'curriculums/{0}/{1}'.format(instance.id, filename)


class Curriculum(models.Model):
    id = models.BigAutoField(primary_key=True)
    th_name = models.CharField(max_length=50, blank=True, default='')
    en_name = models.CharField(max_length=50, blank=True, default='')
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    info = models.CharField(max_length=200, default='')
    attachment_file = models.FileField(upload_to=curriculum_attachment_file_directory_path, null=True, blank=True)

class CurriculumSKillGroup(models.Model):
    curriculum_id_fk = models.ForeignKey(Curriculum, on_delete=models.CASCADE)
    skill_group_id_fk = models.ForeignKey(SkillGroup, on_delete=models.CASCADE)

