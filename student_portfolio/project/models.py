from django.db import models

# Create your models here.

def project_attachment_file_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'projects/{0}/{1}'.format(instance.projectId, filename)

class Project(models.Model):
    projectId = models.BigAutoField(primary_key=True)

    title = models.CharField(max_length=100)
    start_date = models.DateField(null=True, blank=False)
    end_date = models.DateField(null=True, blank=False)

    #consider adding more staffs.
    mainStaffId = models.CharField(max_length=11, blank=True, default='')
    info = models.CharField(max_length=200, blank=True, default='')

    skills = models.JSONField(default=dict)

    # user_id
    proposed_by = models.BigIntegerField(null=False, editable=False)

    approved = models.BooleanField(default=False)
    approved_by = models.BigIntegerField(null=True)
    used_for_calculation = models.BooleanField(default=False)

    attachment_link = models.URLField(max_length=200, blank=True, default='')
    attachment_file = models.FileField(upload_to=project_attachment_file_directory_path, null=True, blank=True)