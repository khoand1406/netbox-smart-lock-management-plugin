from dcim.models.racks import Rack
from dcim.models.sites import Location, Region, Site
from extras.models.tags import Tag
from netbox.forms.bulk_import import PrimaryModelImportForm
from utilities.forms.fields.csv import CSVModelMultipleChoiceField
from utilities.forms.fields.csv import CSVModelChoiceField, CSVChoiceField
from .models import RackFaceChoices, SmartLock, SmartLockStatusChoices
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
class SmartLockBulkImportCSVForm(PrimaryModelImportForm):
    status= CSVChoiceField(
        choices= SmartLockStatusChoices,
        label= _("Status"),
        help_text= _("Operation Status")
    )
    region = CSVModelChoiceField(
        queryset=Region.objects.all(),
        to_field_name="name",
        required=False,
        label=_("Region"),
        help_text=_("Assigned Region")
    )

    site = CSVModelChoiceField(
        queryset=Site.objects.all(),
        to_field_name="name",
        required=True,
        label=_("Site"),
        help_text=_("Assigned Site")
    )

    location = CSVModelChoiceField(
        queryset=Location.objects.all(),
        to_field_name="name",
        required=True,
        label=_("Location"),
        help_text=_("Location")
    )

    rack = CSVModelChoiceField(
        queryset=Rack.objects.all(),
        to_field_name="name",
        required=False,
        label=_("Rack"),
        help_text=_("Assigned Rack")
    )
    rack_face= CSVChoiceField(
        choices=RackFaceChoices,
        label= _("Rack Face"),
        required=False,
        help_text= _("Rack Face")
    )
    tags = CSVModelMultipleChoiceField(
        queryset=Tag.objects.filter(
            object_types=ContentType.objects.get_for_model(model= SmartLock)
        ) | Tag.objects.filter(object_types__isnull=True),
        to_field_name="name",
        required=False,
        label=_("Tags"),
        help_text=_("Comma-separated list of tag names"),
    )

    class Meta:
        model = SmartLock
        fields = (
            "name",
            "code",
            "status",
            "description",
            "device_type",
            "manufacturer",
            "model",
            "serial",
            "installation_date",
            "purchase_date",
            "warranty_period",
            "region",
            "site",
            "location",
            "rack",
            "rack_face",
            "tags"
        )
    