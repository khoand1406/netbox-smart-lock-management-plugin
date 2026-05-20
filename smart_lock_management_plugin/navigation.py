"""
Navigation menu items for smart_lock_management_plugin.

For more information on navigation menus, see:
https://docs.netbox.dev/en/stable/plugins/development/navigation/
"""


from netbox.plugins.navigation import PluginMenu, PluginMenuButton, PluginMenuItem
from django.utils.translation import gettext_lazy as _

menu = PluginMenu(
    label=_("Physical Security Devices"),
    groups=(
        (
            _("Device Management"),
            (
                PluginMenuItem(
                    link="plugins:smart_lock_management_plugin:smartlock_list",
                    link_text=_("Smart Lock Management"),
                    permissions=[
                        "smart_lock_management_plugin.view_smartlock"
                    ],
                    buttons=(
                        PluginMenuButton(
                            link="plugins:smart_lock_management_plugin:smartlock_add",
                            title=_("Add"),
                            icon_class="mdi mdi-plus-thick",
                            permissions=[
                                "smart_lock_management_plugin.add_smartlock"
                            ],
                        ),
                    ),
                ),
            ),
        ),
    ),
)