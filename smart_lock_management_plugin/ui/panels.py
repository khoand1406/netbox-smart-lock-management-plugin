from netbox.ui import attrs, panels


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