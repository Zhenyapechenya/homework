from django_filters.rest_framework import DateFromToRangeFilter, FilterSet

from advertisements.models import Advertisement



class AdvertisementFilter(FilterSet):
    created_at = DateFromToRangeFilter()

    class Meta:
        model = Advertisement
        fields = ['creator', 'created_at', 'status']
