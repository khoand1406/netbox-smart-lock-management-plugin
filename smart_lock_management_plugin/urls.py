"""
URL patterns for smart_lock_management_plugin.

For more information on URL routing, see:
https://docs.netbox.dev/en/stable/plugins/development/views/#url-registration

For Django URL patterns, see:
https://docs.djangoproject.com/en/stable/topics/http/urls/
"""

from django.urls import path
from netbox.views.generic import ObjectChangeLogView

from . import models, views

urlpatterns = (
    path("smart-locks/", views.SmartLockListView.as_view(), name="smartlock_list"),
    path("smart-locks/add/", views.SmartLockCreateView.as_view(), name="smartlock_add"),
    path("smart-locks/<int:pk>/", views.SmartLockView.as_view(), name="smartlock"),
    path("smart-locks/<int:pk>/edit/", views.SmartLockEditView.as_view(), name="smartlock_edit"),
    path("smart-locks/<int:pk>/delete/", views.SmartLockDeleteView.as_view(), name="smartlock_delete"),
    path("smart-locks/<int:pk>/images", views.SmartLockImageView.as_view(), name="smartlock_image-attachments"),
    path(
        "smart-locks/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="smartlock_changelog",
        kwargs={"model": models.SmartLock},
    ),
    path("smart-locks/edit", views.SmartLockBulkEditView.as_view(), name="smartlock_bulk_edit"),
    path("smart-locks/delete", views.SmartLockBulkDeleteView.as_view(), name="smartlock_bulk_delete"),
    path("smart-locks/import", views.SmartLockBulkImportView.as_view(), name= "smartlock_bulk_import")
)
