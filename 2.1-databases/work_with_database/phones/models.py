from django.db import models


class Phone(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    image = models.ImageField()
    release_date = models.DateField(auto_now=True)
    lte_exists = models.BooleanField()
    slug = models.SlugField(max_length=200, unique=True)
