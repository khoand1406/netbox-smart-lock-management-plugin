"""
Tables for smart_lock_management_plugin.

For more information on NetBox tables, see:
https://docs.netbox.dev/en/stable/plugins/development/tables/

For django-tables2 documentation, see:
https://django-tables2.readthedocs.io/
"""

import django_tables2 as tables
from netbox.tables import NetBoxTable, columns
from django.utils.translation import gettext_lazy as _
from .models import SmartLock

class SmartLockTable(NetBoxTable):
    """
    Table definition cho danh sách Smart Lock
    """
    
    name = tables.Column(
        verbose_name=_('Name'),
        linkify=True
    )
    
    code = tables.Column(
        verbose_name=_('Code')
    )
    
    status = columns.ChoiceFieldColumn(
        
        verbose_name=_('Status')
    )
    
    site = tables.Column(
        verbose_name=_('Site'),
        linkify= True
    )
    
    location = tables.Column(
        verbose_name=_('Location'),
        linkify=True
    )
    
    rack = tables.Column(
        verbose_name=_('Rack'),
        linkify=True
    )
    
    manufacturer = tables.Column(
        verbose_name=_('Manufacturer')
    )
    
    device_type = tables.Column(
        verbose_name=_('Device Type')
    )
    
    created = columns.DateTimeColumn(
    verbose_name=_("Created"),
    )
    
    created_by = tables.Column(
        verbose_name=_('Created By')
    )

    last_updated = tables.DateTimeColumn(
    verbose_name=_("Last Updated"),
    format="Y-m-d H:i:s"
    )
    
    
    class Meta(NetBoxTable.Meta):
        model = SmartLock
        fields = (
            'name', 'code', 'status', 'site', 'location', 'rack',
            'manufacturer', 'device_type', 'created', 'created_by', 'last_updated', 'actions'
        )
        default_columns = (
            'name', 'code', 'status','site', 'location', 'rack',
            'manufacturer', 'device_type','created', 'created_by', 'last_updated', 'actions'
        )
