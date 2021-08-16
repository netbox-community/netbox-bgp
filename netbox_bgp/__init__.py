from extras.plugins import PluginConfig
from .version import __version__


class BGPConfig(PluginConfig):
    name = 'netbox_bgp'
    verbose_name = 'BGP'
    description = 'Subsystem for tracking bgp related objects'
    version = __version__
    author = 'Nikolay Yuzefovich'
    author_email = 'mgk.kolek@gmail.com'
    base_url = 'bgp'
    required_settings = []
    min_version = '2.10.1'
    max_version = '2.11.11'
    default_settings = {
        'device_ext_page': 'right'
    }


config = BGPConfig # noqa
