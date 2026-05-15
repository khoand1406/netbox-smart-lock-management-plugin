"""
smart_lock_management_plugin

Plugin configuration for smart_lock_management_plugin.

For a complete list of PluginConfig attributes, see:
https://docs.netbox.dev/en/stable/plugins/development/#pluginconfig-attributes
"""

__author__ = """Khoa Nguyen"""
__email__ = "nguyenkhoa14022002@gmail.com"
__version__ = "0.1.0"




from netbox.plugins import PluginConfig

class Smart_Lock_Management_PluginConfig(PluginConfig):
    name = "smart_lock_management_plugin"
    verbose_name = "smart_lock_management_plugin"
    description = "Plugin for smart lock management"
    author= "Khoa Nguyen"
    author_email = "nguyenkhoa14022002@gmail.com"
    version = __version__
    base_url = "smart_lock_management_plugin"
    min_version = "4.5.0"
    max_version = "4.5.99"
    graphql_schema = "graphql.schema"

config = Smart_Lock_Management_PluginConfig
