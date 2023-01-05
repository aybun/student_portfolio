import datetime

from django.db import models
from event.models import Skill
from django.contrib.auth.models import User
import django

def project_attachment_file_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'projects/{0}/{1}'.format(instance.id, filename)


class Project(models.Model):
    id = models.BigAutoField(primary_key=True)

    title = models.CharField(max_length=100)
    start_date = models.DateField(default=django.utils.timezone.now(), blank=False)
    end_date = models.DateField(default=django.utils.timezone.now(), blank=False)

    info = models.CharField(max_length=200, blank=True, default='')

    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL,
                                   related_name='project_created_by_set', editable=False)

    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL,
                                    related_name='project_approved_by_set', editable=False)

    used_for_calculation = models.BooleanField(default=False)

    attachment_link = models.URLField(max_length=200, blank=True, default='')
    attachment_file = models.FileField(upload_to=project_attachment_file_directory_path, null=True, blank=True)

    skills = models.ManyToManyField(Skill, related_name='project_skill_set', null=True)
    staffs = models.ManyToManyField(User, related_name='project_staff_set', null=True)

    def __str__(self):
        return "{} {}".format(self.id, self.title)
