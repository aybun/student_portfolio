from django.db import models

# Create your models here.
class Student(models.Model):
    id = models.BigAutoField(primary_key=True)
    studentId  = models.CharField( max_length=11)
    userId = models.BigIntegerField()
    firstname   = models.CharField(max_length=50, blank=True)
    middlename  = models.CharField(max_length=50, blank=True)
    lastname    = models.CharField(max_length=50, blank=True)

