from django.db import models

# Create your models here.
class Package(models.Model):
    name = models.CharField(max_length= 30)
    duration = models.CharField(max_length = 20)
    price = models.CharField(max_length=20)
    destination = models.CharField(max_length=20)
    #Activity - (
     #       Cultural / Natural Beauty / Pilgrimage / Adventure /
    #Wildlife / Rafting / Trekking
    #)
    #
    activity = models.CharField(max_length=40)
    cost_included = models.TextField()
    cost_excluded = models.TextField()
    season = models.CharField(max_length=30, blank=True, null= True)
    #description = models.TextField()

    #photo = models.ImageField(upload_to = /images/)

    def __str__(self):
        return self.name




