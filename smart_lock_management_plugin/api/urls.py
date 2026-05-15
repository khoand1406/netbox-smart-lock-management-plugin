"""
API URL patterns for smart_lock_management_plugin.

For more information on NetBox REST API routing, see:
https://docs.netbox.dev/en/stable/plugins/development/rest-api/#routers

For Django REST Framework routers, see:
https://www.django-rest-framework.org/api-guide/routers/
"""

from netbox.api.routers import NetBoxRouter

from .views import SmartLockViewSet

app_name = "smart_lock_management_plugin"

router = NetBoxRouter()
router.register("smart-lock-management-plugins", SmartLockViewSet)

urlpatterns = router.urls

