"""
API serializers for smart_lock_management_plugin.

Serializers are required for NetBox event handling (webhooks, change logging).
They also power the REST API endpoints.

For more information on NetBox REST API serializers, see:
https://docs.netbox.dev/en/stable/plugins/development/rest-api/#serializers

For Django REST Framework serializers, see:
https://www.django-rest-framework.org/api-guide/serializers/
"""

from netbox.api.serializers import NetBoxModelSerializer
from rest_framework import serializers

from ..models import SmartLock


class SmartLockSerializer(NetBoxModelSerializer):
    
    class Meta:
        model = SmartLock
        fields = "__all__"
