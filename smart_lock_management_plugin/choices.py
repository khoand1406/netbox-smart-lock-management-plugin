from utilities.choices import ChoiceSet
from django.utils.translation import gettext_lazy as _

class SmartLockStatusChoices(ChoiceSet):
    key = "SmartLock.status"

    STATUS_ACTIVE = "active"
    STATUS_INACTIVE = "inactive"
    STATUS_MAINTENANCE = "maintenance"
    STATUS_FAULT = "fault"

    CHOICES = [
        (STATUS_ACTIVE, _("Active")),
        (STATUS_INACTIVE, _("Inactive")),
        (STATUS_MAINTENANCE, _("Maintenance")),
        (STATUS_FAULT, _("Fault")),
    ]

    DEFAULT = STATUS_ACTIVE
    
class RackFaceChoices(ChoiceSet):
    """Choices for Rack Face"""
    
    FACE_FRONT = 'front'
    FACE_REAR = 'rear'
    
    CHOICES = [
        (FACE_FRONT, _('front')),
        (FACE_REAR, _('rear')),
    ]