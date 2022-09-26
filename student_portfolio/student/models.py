from django.db import models

# Create your models here.
class Student(models.Model):
    id = models.BigAutoField(primary_key=True)

    studentId  = models.CharField(max_length=11, blank=True, default='')
    userId = models.BigIntegerField(null=True)

    firstname   = models.CharField(max_length=50, blank=True, default='')
    middlename  = models.CharField(max_length=50, blank=True, default='')
    lastname    = models.CharField(max_length=50, blank=True, default='')

