from dcim.models.racks import Rack
from dcim.models.sites import Location, Region, Site
from extras.models.tags import Tag
from netbox.forms.bulk_edit import NetBoxModelBulkEditForm
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from utilities.forms.fields.dynamic import DynamicModelMultipleChoiceField
from utilities.forms.rendering import FieldSet
from utilities.forms.fields.dynamic import DynamicModelChoiceField
from utilities.forms.utils import add_blank_choice
from .models import RackFaceChoices, SmartLock, SmartLockStatusChoices

class SmartLockBulkEditForm(NetBoxModelBulkEditForm):
    model = SmartLock

    pk = forms.ModelMultipleChoiceField(
        queryset=SmartLock.objects.all(),
        widget=forms.MultipleHiddenInput,
    )

    status = forms.ChoiceField(
        label=_("Status"),
        choices=add_blank_choice(
            SmartLockStatusChoices
        ),
        required=False,
        initial="",
    )

    device_type = forms.CharField(
        label=_("Device Type"),
        required=False,
        max_length=100,
    )

    manufacturer = forms.CharField(
        label=_("Manufacturer"),
        required=False,
        max_length=200,
    )

    
    serial = forms.CharField(
        label=_("Serial"),
        required=False,
        max_length=100,
    )

    region = DynamicModelChoiceField(
        queryset=Region.objects.all(),
        label=_("Region"),
        required=False,
    )

    site = DynamicModelChoiceField(
        queryset=Site.objects.all(),
        label=_("Site"),
        required=False,
        query_params={
            "region_id": "$region",
        },
    )

    location = DynamicModelChoiceField(
        queryset=Location.objects.all(),
        label=_("Location"),
        required=False,
        query_params={
            "site_id": "$site",
        },
    )

    rack = DynamicModelChoiceField(
        queryset=Rack.objects.all(),
        label=_("Rack"),
        required=False,
        query_params={
            "location_id": "$location",
        },
    )

    rack_face = forms.ChoiceField(
        label=_("Rack Face"),
        choices=add_blank_choice(
            RackFaceChoices
        ),
        required=False,
        initial="",
    )
    add_tags = DynamicModelMultipleChoiceField(
        queryset=Tag.objects.filter(
            object_types=ContentType.objects.get_for_model(SmartLock)
        ) | Tag.objects.filter(object_types__isnull=True),
        required=False,
        label=_("Add Tags"),
    )

    remove_tags = DynamicModelMultipleChoiceField(
        queryset=Tag.objects.filter(
            object_types=ContentType.objects.get_for_model(SmartLock)
        ) | Tag.objects.filter(object_types__isnull=True),
        required=False,
        label=_("Remove Tags"),
    )

    nullable_fields = (
        "description",
        "manufacturer",
        "serial",
        "installation_date",
        "purchase_date",
        "warranty_period",
        "region",
        "rack",
        "rack_face",
    )

    fieldsets = (
    FieldSet(
        "status",
        "description",
        "device_type",
        "manufacturer",
        "serial",
        name=_("Basic Information"),
    ),
    FieldSet(
        "region",
        "site",
        "location",
        "rack",
        "rack_face",
        name=_("Location Information"),
    ),
    FieldSet(
            "add_tags",
            "remove_tags",
            name=_("Tags"),
    )
    )

    
    