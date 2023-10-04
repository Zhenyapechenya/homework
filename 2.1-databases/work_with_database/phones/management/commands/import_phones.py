import csv

from django.core.management.base import BaseCommand
# from autoslug import AutoSlugField
from django.utils.text import slugify

from phones.models import Phone


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open('phones.csv', 'r') as file:
            phones = list(csv.DictReader(file, delimiter=';'))

        for phone in phones:
            p = Phone.objects.create(id=phone.get('id'), name=phone.get('name'), 
                                    image=phone.get('image'), price=phone.get('price'),
                                    release_date=phone.get('release_date'), 
                                    lte_exists=phone.get('lte_exists'), slug = slugify(phone.get('name'))
                                    )
