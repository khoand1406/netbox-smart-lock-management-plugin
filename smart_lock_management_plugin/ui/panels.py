from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from netbox.ui.panels import Panel
from netbox.ui import attrs, panels, actions
from django.contrib.contenttypes.models import ContentType
from upload_file_plugin.models import UploadedFile
class SmartLockPanel(panels.ObjectAttributesPanel):
    name = _("Detail Information")
    slug = "smartlock_details"

    name_attr = attrs.TextAttr("name", label=_("Name"))
    code = attrs.TextAttr("code", label=_("Code"))
    status = attrs.ChoiceAttr("status", label=_("Status"))
    description = attrs.TextAttr("description", label=_("Description"))
    device_type = attrs.TextAttr("device_type", label=_("Device Type"))
    manufacturer = attrs.TextAttr("manufacturer", label=_("Manufacturer"))
    model = attrs.TextAttr("model", label=_("Model"))
    serial = attrs.TextAttr("serial", label=_("Serial"))
    region = attrs.RelatedObjectAttr("region", linkify=True, label=_("Region"))
    site = attrs.RelatedObjectAttr("site", linkify=True, label=_("Site"))
    location = attrs.RelatedObjectAttr("location", linkify=True, label=_("Location"))
    rack = attrs.RelatedObjectAttr("rack", linkify=True, label=_("Rack"))
    rack_face = attrs.ChoiceAttr("rack_face", label=_("Rack Face"))
    installation_date = attrs.TextAttr("installation_date", label=_("Installation Date"))
    purchase_date = attrs.TextAttr("purchase_date", label=_("Purchase Date"))
    warranty_period_months = attrs.NumericAttr("warranty_period_months", label=_("Warranty Period (months)"))
    warranty_expiration_date = attrs.TextAttr("warranty_expiration_date", label=_("Warranty Expires Date"))
    created_by = attrs.RelatedObjectAttr("created_by", linkify=True, label=_("Created By"))
    created = attrs.DateTimeAttr("created", label=_("Created"))
    last_updated = attrs.DateTimeAttr("last_updated", label=_("Last Updated"))
    
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
                "model_name": lambda ctx: ctx["object"]._meta.model_name,
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
            "model_name":obj._meta.model_name
        }
        