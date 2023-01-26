from datetime import datetime

from django.db import models
import django
from django.contrib.auth.models import User


# Create your models here.
from event.models import Skill

def award_attachment_file_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'awards/{0}/{1}'.format(instance.id, filename)

class Award(models.Model):
    id = models.BigAutoField(primary_key=True)

    title = models.CharField(max_length=100)
    rank = models.IntegerField(default=0)

    received_date = models.DateField(default=django.utils.timezone.now, blank=False)


    info = models.CharField(max_length=200, blank=True, default='')

    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL,
                                   related_name='award_created_by_set', editable=False)

    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL,
                                    related_name='award_approved_by_set', editable=True, blank=True)

    used_for_calculation = models.BooleanField(default=False)

    attachment_link = models.URLField(max_length=200, blank=True, default='')
    attachment_file = models.FileField(upload_to=award_attachment_file_directory_path, null=True, blank=True)

    #Many to Many fields
    skills = models.ManyToManyField(Skill, related_name='award_skill_set', null=True)
    receivers = models.ManyToManyField(User, related_name='award_receiver_set', null=True)
    supervisors = models.ManyToManyField(User, related_name='award_supervisor_set', null=True)

    def __str__(self):
        return "{} {}".format(self.id, self.title)