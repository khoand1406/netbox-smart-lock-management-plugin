"""
Filtersets for smart_lock_management_plugin.

For more information on NetBox filtersets, see:
https://docs.netbox.dev/en/stable/plugins/development/filtersets/

For django-filters documentation, see:
https://django-filter.readthedocs.io/
"""

import django_filters
from django.db.models import Q
from dcim.models.racks import Rack
from dcim.models.sites import Location, Region, Site
from extras.filters import TagFilter
from netbox.filtersets import NetBoxModelFilterSet
from utilities.filtersets import register_filterset

from .models import SmartLock

@register_filterset
class SmartLockFilterSet(NetBoxModelFilterSet):
    q = django_filters.CharFilter(
        method="search",
        label="Search",
    )

    status = django_filters.MultipleChoiceFilter(
        choices=SmartLock._meta.get_field("status").choices,
    )

    region = django_filters.ModelMultipleChoiceFilter(
        queryset=Region.objects.all(),
        field_name="region",
        label="Region",
    )

    site = django_filters.ModelMultipleChoiceFilter(
        queryset=Site.objects.all(),
    )

    location = django_filters.ModelMultipleChoiceFilter(
        queryset=Location.objects.all(),
    )

    rack = django_filters.ModelMultipleChoiceFilter(
        queryset=Rack.objects.all(),
    )
    tag= TagFilter()

    class Meta:
        model = SmartLock
        fields = (
            "q",
            "status",
            "region",
            "site",
            "location",
            "rack",
            "tag",
        )

    def search(self, queryset, name, value):
        """
        Tìm kiếm theo nhiều trường.
        """
        if not value:
            return queryset

        return queryset.filter(
            Q(name__icontains=value)
            | Q(code__icontains=value)
            | Q(description__icontains=value)
            | Q(manufacturer__icontains=value)
            | Q(device_type__icontains=value)
            | Q(serial__icontains=value)
        )