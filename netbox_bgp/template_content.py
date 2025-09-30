from dcim.models import Device
from django.conf import settings
from netbox.plugins import PluginTemplateExtension
from netbox.views.generic import ObjectChildrenView
from utilities.views import ViewTab, register_model_view

from .filtersets import BGPSessionFilterSet
from .models import BGPSession
from .tables import BGPSessionTable

# Load configuration
config = getattr(settings, "PLUGINS_CONFIG", {}).get("netbox_bgp", {})

# Only register the tab view if configuration is set to 'tab'
if config.get("device_ext_page", "") == "tab":

    @register_model_view(Device, name="bgp_sessions", path="bgp-sessions")
    class DeviceBGPSessionTabView(ObjectChildrenView):
        """View to display BGP sessions for this device in a tab."""

        queryset = Device.objects.all()
        child_model = BGPSession
        filterset = BGPSessionFilterSet
        table = BGPSessionTable
        template_name = "generic/object_children.html"
        hide_if_empty = False
        tab = ViewTab(
            label="BGP Sessions",
            badge=lambda obj: BGPSession.objects.filter(device=obj).count(),
            permission="netbox_bgp.view_bgpsession",
        )

        def get_children(self, request, parent):
            """Get BGP sessions for this device."""
            return BGPSession.objects.filter(device=parent)


@register_model_view(IPAddress, name="bgp-sessions", path="bgp-sessions")
class IPAddressBGPSessionsView(generic.ObjectChildrenView):
    """View to display BGP sessions associated with an IP address."""

    queryset = IPAddress.objects.all()
    child_model = BGPSession
    filterset = BGPSessionFilterSet
    table = BGPSessionTable
    template_name = "generic/object_children.html"
    hide_if_empty = False

    @staticmethod
    def _get_ip_bgp_sessions(ip_address: IPAddress) -> QuerySet[BGPSession]:
        """Helper to get BGP sessions related to an IP address."""
        return BGPSession.objects.filter(
            Q(local_address=ip_address) | Q(remote_address=ip_address)
        ).distinct()

    tab = ViewTab(
        label="BGP Sessions",
        badge=lambda obj: IPAddressBGPSessionsView._get_ip_bgp_sessions(obj).count(),
        permission="netbox_bgp.view_bgpsession",
    )

    def get_children(
        self, request: HttpRequest, parent: IPAddress
    ) -> QuerySet[BGPSession]:
        """Get BGP sessions where the IP address is either the local or remote address."""
        return IPAddressBGPSessionsView._get_ip_bgp_sessions(parent)


class DeviceBGPSession(PluginTemplateExtension):
    models = ("dcim.device",)

    def left_page(self):
        if self.context["config"].get("device_ext_page") == "left":
            return self.x_page()
        return ""

    def right_page(self):
        if self.context["config"].get("device_ext_page") == "right":
            return self.x_page()
        return ""

    def full_width_page(self):
        if self.context["config"].get("device_ext_page") == "full_width":
            return self.x_page()
        return ""

    def x_page(self):
        return self.render(
            "netbox_bgp/device_extend.html",
        )


template_extensions = [DeviceBGPSession]
