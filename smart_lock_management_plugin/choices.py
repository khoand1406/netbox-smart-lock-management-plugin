from utilities.choices import ChoiceSet


class SmartLockStatusChoices(ChoiceSet):
    key = "SmartLock.status"

    STATUS_ACTIVE = "active"
    STATUS_INACTIVE = "inactive"
    STATUS_MAINTENANCE = "maintenance"
    STATUS_FAULT = "fault"

    CHOICES = [
        (STATUS_ACTIVE, "Active"),
        (STATUS_INACTIVE, "Inactive"),
        (STATUS_MAINTENANCE, "Maintenance"),
        (STATUS_FAULT, "Fault"),
    ]

    DEFAULT = STATUS_ACTIVE
    
class RackFaceChoices(ChoiceSet):
    """Choices for Rack Face"""
    
    FACE_FRONT = 'front'
    FACE_REAR = 'rear'
    
    CHOICES = [
        (FACE_FRONT, 'front'),
        (FACE_REAR, 'rear'),
    ]