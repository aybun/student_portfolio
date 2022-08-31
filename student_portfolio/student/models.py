from django.db import models

# Create your models here.
class Student(models.Model):
    id = models.BigAutoField(primary_key=True)
    studentId  = models.CharField( max_length=11) #no hyphen

    firstname   = models.CharField(max_length=50, blank=False)
    middlename  = models.CharField(max_length=50, blank=False)
    lastname    = models.CharField(max_length=50, blank=False)

