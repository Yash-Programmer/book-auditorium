from django.db import models

# Create your models here.
class Entry(models.Model):
    name = models.CharField(max_length=1000)
    email = models.CharField(max_length=100000)
    adm_no = models.IntegerField(max_length=6)
    class_sec = models.CharField(max_length=1000)
    parent = models.CharField(max_length=1000)

    def __str__(self):
        return self.email
         