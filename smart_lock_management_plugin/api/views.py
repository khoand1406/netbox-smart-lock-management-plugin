"""
API viewsets for smart_lock_management_plugin.

For more information on NetBox REST API viewsets, see:
https://docs.netbox.dev/en/stable/plugins/development/rest-api/#viewsets

For Django REST Framework viewsets, see:
https://www.django-rest-framework.org/api-guide/viewsets/
"""



from netbox.api.viewsets import NetBoxModelViewSet

from ..models import SmartLock
from .serializers import SmartLockSerializer


class SmartLockViewSet(NetBoxModelViewSet):
    queryset = SmartLock.objects.all()
    serializer_class = SmartLockSerializer
    

