"""
Forms for smart_lock_management_plugin.

For more information on NetBox forms, see:
https://docs.netbox.dev/en/stable/plugins/development/forms/
"""

from dcim.models.racks import Rack
from dcim.models.sites import Location, Region, Site
from extras.models.models import ImageAttachment
from extras.models.tags import Tag
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from django import forms
from django.core.validators import FileExtensionValidator
from django.contrib.contenttypes.models import ContentType
from utilities.forms.fields.fields import TagFilterField
from utilities.forms.rendering import FieldSet
from utilities.forms.fields.dynamic import DynamicModelMultipleChoiceField
from utilities.forms.fields.dynamic import DynamicModelChoiceField
from .models import RackFaceChoices, SmartLock
from .ui.widgets import CustomUploadWidget, MultipleFileInput, MultipleFileField


class SmartLockForm(NetBoxModelForm):
    attachment= MultipleFileField(
        required= False,
        label= "Attachment",
        help_text="Only jpg, jpeg, png allowed. Maximum total size per file: 25MB.",
        validators=[
            FileExtensionValidator(["jpg", "jpeg", "png"])
        ],
        widget=CustomUploadWidget(
           attrs= {
               "multiple": True
           }
        )
    )
    
    
    region = DynamicModelChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label="Region",
    )

   
    site = DynamicModelChoiceField(
        queryset=Site.objects.all(),
        required=True,
        label="Site",
        query_params={
        "region_id": "$region",
    },
    )

    
    location = DynamicModelChoiceField(
        queryset=Location.objects.all(),
        required=True,
        label="Location",
        query_params={
        "site_id": "$site",
    },
    )

    
    rack = DynamicModelChoiceField(
        queryset=Rack.objects.all(),
        required=False,
        label="Rack",
        query_params={
        "location_id": "$location",
    },
    )

    
    installation_date = forms.DateField(
        required=False,
        label="Installation Date",
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "placeholder": "DD/MM/YYYY",
            }
        ),
    )

    purchase_date = forms.DateField(
        required=False,
        label="Purchase Date",
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "placeholder": "DD/MM/YYYY",
            }
        ),
    )

    warranty_expiration_date = forms.DateField(
        required=False,
        label="Warranty Expiration Date",
        disabled=True,
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "placeholder": "DD/MM/YYYY",
            }
        ),
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
        labels = {
            "name":"Name",
            "code":"Code",
            "status":"Status",
            "description":"Description",
            "device_type":"Device Type",
            "attachment":"Attachment",
            "manufacturer":"Manufacturer",
            "model":"Model",
            "serial":"Serial",
            "installation_date":"Installation Date",
            "purchase_date":"Purchase Date",
            "warranty_period": "Warranty Period",
            "region":"Region",
            "site":"Site",
            "location":"Location",
            "rack":"Rack",
            "rack_face":"Rack Face",
            "tags":"Tags"
        }
        help_texts = {
            "name": "Allow up to 100 characters.",
            "code": "Allow up to 50 characters. Unique value.",
            "status": "Default is Active.",
            "description": "Allow up to 500 characters.",
            "device_type":"Allow up to 100 characters",
            "attachment": "Only jpg, jpeg, png allowed. Maximum size 25MB.",
            "warranty_period_months": "Enter a positive integer (unit: months).",
        }
    def clean_attachment(self):
        files = self.files.getlist("attachment")

        if not files:
            return []

        allowed_extensions = {"jpg", "jpeg", "png"}
        max_size = 25 * 1024 * 1024

        for file in files:
            
            if file.size > max_size:
                raise forms.ValidationError(
                    f"File '{file.name}' exceeds 25MB."
                )

            
            extension = file.name.rsplit(".", 1)[-1].lower()
            if extension not in allowed_extensions:
                raise forms.ValidationError(
                    f"File '{file.name}' has unsupported extension."
                )

        return files
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        region_id = self.data.get("region") or getattr(self.instance, "region_id", None)
        site_id = self.data.get("site") or getattr(self.instance, "site_id", None)
        location_id = self.data.get("location") or getattr(self.instance, "location_id", None)

        if not region_id:
            self.fields["site"].queryset = Site.objects.none()
        else:
            self.fields["site"].queryset = Site.objects.filter(region_id=region_id)

        if not site_id:
            self.fields["location"].queryset = Location.objects.none()
        else:
            self.fields["location"].queryset = Location.objects.filter(site_id=site_id)

        if not location_id:
            self.fields["rack"].queryset = Rack.objects.none()
        else:
            self.fields["rack"].queryset = Rack.objects.filter(location_id=location_id)
            
class SmartLockEditForm(NetBoxModelForm):
   
    attachment = MultipleFileField(
        required=False,
        label="New Attachments",
        help_text="Only jpg, jpeg, png allowed. Maximum total size per file: 25MB.",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png"]
            )
        ],
        widget=CustomUploadWidget(
            attrs={
                "multiple": True
            }
        ),
    )
    region= DynamicModelChoiceField(
        queryset=Region.objects.all(),
        required= True,
        label= "Region"
        
    )
    
    site= DynamicModelChoiceField(
        queryset=Site.objects.all(),
        required= False,
        label="Site",
        query_params={
            "region_id":"$region"
        }
    )
    location= DynamicModelChoiceField(
        queryset= Location.objects.all(),
        required= False,
        label= "Location",
        query_params={
            "site_id":"$site"
        }
    )
    rack= DynamicModelChoiceField(
        queryset= Rack.objects.all(),
        required= False,
        label= "Rack",
        query_params={
            "location_id":"$location"
        }
    )
    
    installation_date = forms.DateField(
        required=False,
        label="Installation Date",
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "placeholder": "DD/MM/YYYY",
            }
        ),
    )

    purchase_date = forms.DateField(
        required=False,
        label="Purchase Date",
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "placeholder": "DD/MM/YYYY",
            }
        ),
    )

    warranty_expiry_date = forms.DateField(
        required=False,
        label="Warranty Expiration Date",
        disabled=True,
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "placeholder": "DD/MM/YYYY",
            }
        ),
    )
    tags = DynamicModelMultipleChoiceField(
        queryset=Tag.objects.filter(
            object_types=ContentType.objects.get_for_model(model=SmartLock)
        ) | Tag.objects.filter(object_types__isnull=True),
        required=False,
        label="Tags",
    )
    
    
    
    class Meta:
        model= SmartLock
        fields= (
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
        labels= {
            "name":"Name",
            "code":"Code",
            "status":"Status",
            "descripiiton":"Description",
            "device_type":"Device Type",
            "manufacturer":"Manufacturer",
            "model":"Model",
            "serial":"Serial",
            "installation_date":"Installation Date",
            "purchase_date":"Purchase Date",
            "region":"Region",
            "site":"Site",
            "location":"Location",
            "rack":"Rack",
            "rack_face": "Rack Face",
            "tags":"Tags"
            
        }
        help_texts={
            "name": "Maximum 100 characters.",
            "code": "Maximum 50 characters and must be unique.",
            "description": "Maximum 500 characters.",
            "attachment": "Upload a new attachment to replace the selected one. Allowed file types: JPG, JPEG, PNG. Maximum size: 25MB.",
            "device_type": "Maximum 100 characters.",
            "warranty_period_months": "Enter a positive integer (unit: months).",
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["warranty_expiry_date"].initial= (
                self.instance.warranty_expiry_date
            )

    def clean_attachment(self):
        
        files = self.files.getlist("attachment")

        if not files:
            return []

        allowed_extensions = {"jpg", "jpeg", "png"}
        max_size = 25 * 1024 * 1024

        for file in files:
            
            if file.size > max_size:
                raise forms.ValidationError(
                    f"File '{file.name}' exceeds 25MB."
                )

            
            extension = file.name.rsplit(".", 1)[-1].lower()
            if extension not in allowed_extensions:
                raise forms.ValidationError(
                    f"File '{file.name}' has unsupported extension."
                )

        return files
    
class SmartLockFilterForm(NetBoxModelFilterSetForm):
    model = SmartLock

    # Search
    q = forms.CharField(
        required=False,
        label="Search",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by name, code, manufacturer...",
            }
        ),
    )

    # Basic Information
    status = forms.MultipleChoiceField(
        required=False,
        choices=SmartLock._meta.get_field("status").choices,
        label="Status",
    )

    # Location Information
    region = DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label="Region",
    )

    site = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        required=False,
        label="Site",
        query_params={
            "region_id": "$region",
        },
    )

    location = DynamicModelMultipleChoiceField(
        queryset=Location.objects.all(),
        required=False,
        label="Location",
        query_params={
            "site_id": "$site",
        },
    )

    rack = DynamicModelMultipleChoiceField(
        queryset=Rack.objects.all(),
        required=False,
        label="Rack",
        query_params={
            "location_id": "$location",
        },
    )

    rack_face = forms.MultipleChoiceField(
        required=False,
        choices=RackFaceChoices,
        label="Rack Face",
    )
    
    tag= TagFilterField(model= SmartLock)

    fieldsets = (
        FieldSet(
            "q",
            name="Search",
        ),
        FieldSet(
            "status",
            "tag",
            name="Basic Information",
        ),
        FieldSet(
            "region",
            "site",
            "location",
            "rack",
            "rack_face",
            name="Location Information",
        ),
    )


    