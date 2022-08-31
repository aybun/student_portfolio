from django.db import models

# Create your models here.
class Staff(models.Model):
    id = models.BigAutoField(primary_key=True)
    staffId  = models.CharField( max_length=11)

    firstname   = models.CharField(max_length=50, blank=False)
    middlename  = models.CharField(max_length=50, blank=False)
    lastname    = models.CharField(max_length=50, blank=False)

