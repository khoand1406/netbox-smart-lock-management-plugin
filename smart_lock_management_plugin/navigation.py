"""
Navigation menu items for smart_lock_management_plugin.

For more information on navigation menus, see:
https://docs.netbox.dev/en/stable/plugins/development/navigation/
"""


from netbox.plugins.navigation import PluginMenu, PluginMenuButton, PluginMenuItem


menu = PluginMenu(
    label="Physical Security Devices",
    groups=(
        (
            "Device Management",
            (
                PluginMenuItem(
                    link="plugins:smart_lock_management_plugin:smartlock_list",
                    link_text="Smart Lock Management",
                    permissions=[
                        "smart_lock_management_plugin.view_smartlock"
                    ],
                    buttons=(
                        PluginMenuButton(
                            link="plugins:smart_lock_management_plugin:smartlock_add",
                            title="Add",
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