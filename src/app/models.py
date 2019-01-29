from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.contrib.contenttypes.fields import GenericRelation
from history.models import History



# Create your models here.
class Package(models.Model):

    name = models.CharField(max_length= 100)
    price = models.IntegerField()
    duration = models.CharField(max_length = 100)
    rating = models.CharField(max_length=100)
    tourtype = models.CharField(max_length=100)
    trekdifficulty = models.CharField(max_length=100)
    operator = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    primary_activity = models.CharField(max_length=100)
    secondary_activity = models.CharField(max_length=100)
    image = models.CharField(max_length=200)
    description = models.TextField()

    like = models.ManyToManyField(User, blank=True)

    cost_included = models.TextField(blank=True,null=True)
    cost_excluded = models.TextField(blank=True,null=True)
    season = models.CharField(max_length=30, blank=True, null= True)

    history = GenericRelation(History, related_name="package")


    def __str__(self):
        return self.name

    def like_count(self):
        return self.like.count()

    def get_absoulte_url(self):
        return reverse('app:detail', kwargs={'pk': self.pk})



