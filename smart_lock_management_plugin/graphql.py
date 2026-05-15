"""
GraphQL schema for smart_lock_management_plugin.

For more information on NetBox GraphQL, see:
https://docs.netbox.dev/en/stable/plugins/development/graphql/

For Strawberry GraphQL documentation, see:
https://strawberry.rocks/
"""

from typing import List

import strawberry
import strawberry_django

from .models import SmartLock


@strawberry_django.type(
    SmartLock,
    fields='__all__',
)
class Smart_Lock_Management_PluginType:
    """GraphQL type for Smart_Lock_Management_Plugin model."""
    pass


@strawberry.type(name="Query")
class Smart_Lock_Management_PluginQuery:
    """GraphQL queries for smart_lock_management_plugin."""

    smartlockmanagementplugin: Smart_Lock_Management_PluginType = strawberry_django.field()
    smartlockmanagementplugin_list: List[Smart_Lock_Management_PluginType] = strawberry_django.field()


schema = [
    Smart_Lock_Management_PluginQuery,
]

