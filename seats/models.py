from django.db import models

# Create your models here.
class Entry(models.Model):
    name = models.CharField(max_length=1000)
    email = models.CharField(max_length=100000)
    adm_no = models.CharField(max_length=6)
    class_sec = models.CharField(max_length=1000)
    parent = models.CharField(max_length=1000)

    def __str__(self):
        return self.adm_no

class Slot_1(models.Model):
    seat_1 = models.CharField(max_length=2)
    seat_2 = models.CharField(max_length=2, null=True, blank=True)
    adm_no = models.CharField(max_length=6)
    # image = models.ImageField(upload_to = 'product-img/', null=True)

    def __str__(self):
        return self.adm_no

         