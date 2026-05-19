from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from netbox.ui.panels import Panel
from netbox.ui import attrs, panels, actions
from django.contrib.contenttypes.models import ContentType
from upload_file_plugin.models import UploadedFile
class SmartLockPanel(panels.ObjectAttributesPanel):
    """
    Panel shows detail infomation of Smart Lock object
    """
    name = "Detail Information"
    
    slug= "smartlock_details"
    
    name_attr= attrs.TextAttr("name")
    code= attrs.TextAttr("code")
    status= attrs.ChoiceAttr("status")
    description= attrs.TextAttr("description")
    device_type= attrs.TextAttr("device_type")
    manufacturer= attrs.TextAttr("manufacturer")
    model= attrs.TextAttr("manufacturer")
    serial= attrs.TextAttr("serial")
    region= attrs.RelatedObjectAttr("region", linkify=True)
    site= attrs.RelatedObjectAttr("site", linkify=True)
    location= attrs.RelatedObjectAttr("location", linkify=True)
    rack= attrs.RelatedObjectAttr("rack", linkify=True)
    rack_face= attrs.ChoiceAttr("rack_face")
    
    installation_date= attrs.TextAttr("installation_date")
    purchase_date= attrs.TextAttr("purchase_date")
    warranty_period_months = attrs.NumericAttr("warranty_period_months")
    warranty_expiration_date = attrs.TextAttr("warranty_expiration_date")
    created_by = attrs.RelatedObjectAttr("created_by", linkify=True)
    created = attrs.DateTimeAttr("created")
    last_updated = attrs.DateTimeAttr("last_updated")
    
class CustomImageAttachentPanels(Panel):
    title = _("Attachments")
    template_name= "smart_lock_management_plugin/panels/custom_image_attachments.html"
    actions = [
        actions.LinkAction(
            view_name="plugins:smart_lock_management_plugin:uploadedfile_add",
            label= _("New Attachment"),
            button_icon= "plus-thick",
            permissions=["upload_file_plugin.add_uploadedfile"],
            
            url_params= {
                "object_id": lambda ctx: ctx["object"].pk,
                "model_name": "SmartLock",
                "return_url": lambda ctx: ctx["object"].get_absolute_url(),
            },
        )
    ]

    def get_context(self, context):
        obj= context["object"]
        print(obj.pk)
        uploaded_files= UploadedFile.objects.filter(
            model_name= "smartlock",
            object_id= obj.pk
        ).order_by("-created_at")
        return {
            **super().get_context(context),
            "uploaded_files": uploaded_files,
            "object": obj,
        }
        