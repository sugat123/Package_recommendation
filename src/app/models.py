from django.db import models

# Create your models here.
class Package(models.Model):

    name = models.CharField(max_length= 100)
    price = models.CharField(max_length=100)
    duration = models.CharField(max_length = 100)
    rating = models.CharField(max_length=100)
    tourtype = models.CharField(max_length=100)
    trekdifficulty = models.CharField(max_length=100)
    operator = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    primary_activity = models.CharField(max_length=100)
    secondary_activty = models.CharField(max_length=100)


    cost_included = models.TextField(blank=True,null=True)
    cost_excluded = models.TextField(blank=True,null=True)
    season = models.CharField(max_length=30, blank=True, null= True)

    def __str__(self):
        return self.name




