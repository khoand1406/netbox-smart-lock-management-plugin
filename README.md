# smart_lock_management_plugin

Plugin for smart lock management


* Free software: MIT
* Documentation: https://.github.io/smart-lock-management-plugin/


## Features

The features the plugin provides should be listed here. For example:

- Manage smart_lock_management_plugin resources through NetBox UI
- Track and organize smart_lock_management_plugin data with custom fields and tags
- REST API endpoints for programmatic access
- GraphQL support for flexible data queries
- Full change logging and journaling support
- Integration with NetBox's permission system
- Global search integration for finding smart_lock_management_plugin objects
- Comprehensive filtering and table views

## Screenshots

<!-- Add screenshots or GIFs demonstrating your plugin's functionality here -->
_Screenshots will be added as features are developed._

## Compatibility

This plugin requires **NetBox 4.5** or later.

| NetBox Version | Plugin Version |
|----------------|----------------|
|     4.5+       |      0.1.0     |

For more detailed compatibility information, see [COMPATIBILITY.md](COMPATIBILITY.md).

## Dependencies

This plugin requires:
- NetBox 0.1.0 or later (NetBox 4.5+)
- Python 3.12 or later

No additional Python packages are required beyond NetBox's core dependencies.

## REST API

This plugin provides a REST API endpoint for managing smart_lock_management_plugin resources:

- `/api/plugins/smart_lock_management_plugin/smart-lock-management-plugins/` - List and create Smart_Lock_Management_Plugin objects


## GraphQL

This plugin provides GraphQL support for querying smart_lock_management_plugin resources through NetBox's GraphQL API.


## Installing

For adding to a NetBox Docker setup see
[the general instructions for using netbox-docker with plugins](https://github.com/netbox-community/netbox-docker/wiki/Using-Netbox-Plugins).

While this is still in development and not yet on pypi you can install with pip:

```bash
pip install git+https://github.com//smart-lock-management-plugin
```

or by adding to your `local_requirements.txt` or `plugin_requirements.txt` (netbox-docker):

```bash
git+https://github.com//smart-lock-management-plugin
```

Enable the plugin in `/opt/netbox/netbox/netbox/configuration.py`,
 or if you use netbox-docker, your `/configuration/plugins.py` file :

```python
PLUGINS = [
    'smart_lock_management_plugin'
]

PLUGINS_CONFIG = {
    "smart_lock_management_plugin": {},
}
```

## Configuration

This plugin does not require any additional configuration by default. Optional configuration parameters can be added to `PLUGINS_CONFIG` in your NetBox configuration file as needed.

## Usage

For detailed usage instructions, please refer to the [documentation](https://.github.io/smart-lock-management-plugin/).

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Reporting Bugs

Please report bugs by opening an issue on our [GitHub Issues](https://github.com//smart-lock-management-plugin/issues) page. When reporting bugs, please include:

- NetBox version
- Plugin version
- Python version
- Steps to reproduce
- Expected behavior
- Actual behavior

### Feature Requests

Feature requests can be submitted as [GitHub Issues](https://github.com//smart-lock-management-plugin/issues) with the "enhancement" label.

## Support

- **Documentation**: https://.github.io/smart-lock-management-plugin/
- **Issues**: https://github.com//smart-lock-management-plugin/issues
- **Discussions**: https://github.com//smart-lock-management-plugin/discussions
- **NetBox Community Slack**: [netdev-community.slack.com](https://netdev.chat/)

## Credits

Based on the NetBox plugin tutorial:

- [demo repository](https://github.com/netbox-community/netbox-plugin-demo)
- [tutorial](https://github.com/netbox-community/netbox-plugin-tutorial)

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [`netbox-community/cookiecutter-netbox-plugin`](https://github.com/netbox-community/cookiecutter-netbox-plugin) project template.
