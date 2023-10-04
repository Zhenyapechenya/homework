from django.db import models
# from autoslug import AutoSlugField
from django.utils.text import slugify


class Phone(models.Model):
    # id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    price = models.FloatField()
    image = models.ImageField()
    release_date = models.DateField(auto_now=True)
    lte_exists = models.BooleanField()
    # slug = models.SlugField(max_length = 200)
    # slug = AutoSlugField(populate_from='name', unique=True)
    slug = models.SlugField(max_length=255, unique=True)
