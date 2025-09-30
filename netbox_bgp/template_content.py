from dcim.models import Device, Interface, Site
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q, QuerySet
from django.http import HttpRequest
from ipam.models import ASN, IPAddress
from netbox.plugins import PluginTemplateExtension
from netbox.views import generic
from tenancy.models import Tenant
from utilities.views import ViewTab, register_model_view
from virtualization.models import VirtualMachine

from .filtersets import BGPSessionFilterSet
from .models import BGPSession
from .tables import BGPSessionTable

# Load configuration
config = getattr(settings, "PLUGINS_CONFIG", {}).get("netbox_bgp", {})

# Only register the tab view if configuration is set to 'tab'
if config.get("device_ext_page", "") == "tab":

    @register_model_view(Device, name="bgp_sessions", path="bgp-sessions")
    class DeviceBGPSessionTabView(generic.ObjectChildrenView):
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


@register_model_view(Site, name="bgp-sessions", path="bgp-sessions")
class SiteBGPSessionsView(generic.ObjectChildrenView):
    """View to display BGP sessions associated with a site."""

    queryset = Site.objects.all()
    child_model = BGPSession
    filterset = BGPSessionFilterSet
    table = BGPSessionTable
    template_name = "generic/object_children.html"
    hide_if_empty = False

    tab = ViewTab(
        label="BGP Sessions",
        badge=lambda obj: BGPSession.objects.filter(site=obj).count(),
        permission="netbox_bgp.view_bgpsession",
    )

    def get_children(self, request: HttpRequest, parent: Site) -> QuerySet[BGPSession]:
        """Get BGP sessions for the site."""
        return BGPSession.objects.filter(site=parent)


@register_model_view(Tenant, name="bgp-sessions", path="bgp-sessions")
class TenantBGPSessionsView(generic.ObjectChildrenView):
    """View to display BGP sessions associated with a tenant."""

    queryset = Tenant.objects.all()
    child_model = BGPSession
    filterset = BGPSessionFilterSet
    table = BGPSessionTable
    template_name = "generic/object_children.html"
    hide_if_empty = False

    tab = ViewTab(
        label="BGP Sessions",
        badge=lambda obj: BGPSession.objects.filter(tenant=obj).count(),
        permission="netbox_bgp.view_bgpsession",
    )

    def get_children(
        self, request: HttpRequest, parent: Tenant
    ) -> QuerySet[BGPSession]:
        """Get BGP sessions for the tenant."""
        return BGPSession.objects.filter(tenant=parent)


@register_model_view(VirtualMachine, name="bgp-sessions", path="bgp-sessions")
class VirtualMachineBGPSessionsView(generic.ObjectChildrenView):
    """View to display BGP sessions associated with a virtual machine."""

    queryset = VirtualMachine.objects.all()
    child_model = BGPSession
    filterset = BGPSessionFilterSet
    table = BGPSessionTable
    template_name = "generic/object_children.html"
    hide_if_empty = False

    tab = ViewTab(
        label="BGP Sessions",
        badge=lambda obj: BGPSession.objects.filter(virtualmachine=obj).count(),
        permission="netbox_bgp.view_bgpsession",
    )

    def get_children(
        self, request: HttpRequest, parent: VirtualMachine
    ) -> QuerySet[BGPSession]:
        """Get BGP sessions for the virtual machine."""
        return BGPSession.objects.filter(virtualmachine=parent)


@register_model_view(ASN, name="bgp-sessions", path="bgp-sessions")
class ASNBGPSessionsView(generic.ObjectChildrenView):
    """View to display BGP sessions associated with an ASN."""

    queryset = ASN.objects.all()
    child_model = BGPSession
    filterset = BGPSessionFilterSet
    table = BGPSessionTable
    template_name = "generic/object_children.html"
    hide_if_empty = False

    @staticmethod
    def _get_asn_bgp_sessions(asn: ASN) -> QuerySet[BGPSession]:
        """Helper to get BGP sessions related to an ASN."""
        return BGPSession.objects.filter(Q(local_as=asn) | Q(remote_as=asn)).distinct()

    tab = ViewTab(
        label="BGP Sessions",
        badge=lambda obj: ASNBGPSessionsView._get_asn_bgp_sessions(obj).count(),
        permission="netbox_bgp.view_bgpsession",
    )

    def get_children(self, request: HttpRequest, parent: ASN) -> QuerySet[BGPSession]:
        """Get BGP sessions where the ASN is either the local or remote AS."""
        return ASNBGPSessionsView._get_asn_bgp_sessions(parent)


@register_model_view(Interface, name="bgp-sessions", path="bgp-sessions")
class InterfaceBGPSessionsView(generic.ObjectChildrenView):
    """View to display BGP sessions associated with an interface."""

    queryset = Interface.objects.all()
    child_model = BGPSession
    filterset = BGPSessionFilterSet
    table = BGPSessionTable
    template_name = "generic/object_children.html"
    hide_if_empty = False

    @staticmethod
    def _get_interface_bgp_sessions(interface: Interface) -> QuerySet[BGPSession]:
        """Helper to get BGP sessions related to an interface via its IP addresses."""
        ct = ContentType.objects.get_for_model(Interface)
        ips = IPAddress.objects.filter(
            assigned_object_type=ct, assigned_object_id=interface.pk
        )
        return BGPSession.objects.filter(
            Q(local_address__in=ips) | Q(remote_address__in=ips)
        ).distinct()

    tab = ViewTab(
        label="BGP Sessions",
        badge=lambda obj: InterfaceBGPSessionsView._get_interface_bgp_sessions(
            obj
        ).count(),
        permission="netbox_bgp.view_bgpsession",
    )

    def get_children(
        self, request: HttpRequest, parent: Interface
    ) -> QuerySet[BGPSession]:
        """Get BGP sessions for the interface."""
        return InterfaceBGPSessionsView._get_interface_bgp_sessions(parent)


# Register only when device_ext_page is set to 'tab';
class DeviceBGPSessionsView(generic.ObjectChildrenView):
    """View to display BGP sessions associated with a device."""

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

    def get_children(
        self, request: HttpRequest, parent: Device
    ) -> QuerySet[BGPSession]:
        """Get BGP sessions for the device."""
        return BGPSession.objects.filter(device=parent)


# Register the BGP sessions tab view only if device_ext_page is set to 'tab';
# otherwise, use the PluginTemplateExtension for inline display (left, right, full_width).
if settings.PLUGINS_CONFIG.get("netbox_bgp", {}).get("device_ext_page") == "tab":
    DeviceBGPSessionsView = register_model_view(
        Device, name="bgp-sessions", path="bgp-sessions"
    )(DeviceBGPSessionsView)


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
