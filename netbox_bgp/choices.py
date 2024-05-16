from utilities.choices import ChoiceSet


class CommunityStatusChoices(ChoiceSet):
    key = "Community.status"

    STATUS_ACTIVE = 'active'
    STATUS_RESERVED = 'reserved'
    STATUS_DEPRECATED = 'deprecated'

    CHOICES = [
        (STATUS_ACTIVE, 'Active', 'blue'),
        (STATUS_RESERVED, 'Reserved', 'cyan'),
        (STATUS_DEPRECATED, 'Deprecated', 'red'),
    ]


class SessionStatusChoices(ChoiceSet):
    key = "Session.status"

    STATUS_OFFLINE = 'offline'
    STATUS_ACTIVE = 'active'
    STATUS_PLANNED = 'planned'
    STATUS_FAILED = 'failed'

    CHOICES = [
        (STATUS_OFFLINE, 'Offline', 'orange'),
        (STATUS_ACTIVE, 'Active', 'green'),
        (STATUS_PLANNED, 'Planned', 'cyan'),
        (STATUS_FAILED, 'Failed', 'red'),
    ]


class ActionChoices(ChoiceSet):
    key = "Action.status"

    CHOICES = [
        ('permit', 'Permit', 'green'),
        ('deny', 'Deny', 'red'),
    ]


class AFISAFIChoices(ChoiceSet):
    key = "AFISAFI.options"

    AFISAFI_IPV4_UNICAST = 'ipv4-unicast'
    AFISAFI_IPV4_MULTICAST = 'ipv4-multicast'
    AFISAFI_IPV4_FLOWSPEC = 'ipv4-flowspec'

    AFISAFI_IPV6_UNICAST = 'ipv6-unicast'
    AFISAFI_IPV6_MULTICAST = 'ipv6-multicast'
    AFISAFI_IPV6_FLOWSPEC = 'ipv6-flowspec'

    AFISAFI_L2VPN_VPLS = 'l2vpn-vpls'
    AFISAFI_L2VPN_EVPN = 'l2vpn-evpn'

    AFISAFI_VPNV4_UNICAST = 'vpnv4-unicast'
    AFISAFI_VPNV4_MULTICAST = 'vpnv4-multicast'
    AFISAFI_VPNV4_FLOWSPEC = 'vpnv4-flowspec'

    AFISAFI_VPNV6_UNICAST = 'vpnv6-unicast'
    AFISAFI_VPNV6_MULTICAST = 'vpnv6-multicast'
    AFISAFI_VPNV6_FLOWSPEC = 'vpnv6-flowspec'

    CHOICES = [
        (AFISAFI_IPV4_UNICAST, 'IPv4 Unicast'),
        (AFISAFI_IPV4_MULTICAST, 'IPv4 Multicast'),
        (AFISAFI_IPV4_FLOWSPEC, 'IPv4 Flowspec'),
        (AFISAFI_IPV6_UNICAST, 'IPv6 Unicast'),
        (AFISAFI_IPV6_MULTICAST, 'IPv6 Multicast'),
        (AFISAFI_L2VPN_VPLS, 'L2VPN VPLS'),
        (AFISAFI_L2VPN_EVPN, 'L2VPN EVPN'),
        (AFISAFI_VPNV4_UNICAST, 'VPNv4 Unicast'),
        (AFISAFI_VPNV4_MULTICAST, 'VPNv4 Multicast'),
        (AFISAFI_VPNV4_FLOWSPEC, 'VPNv4 Flowspec'),
        (AFISAFI_VPNV6_UNICAST, 'VPNv6 Unicast'),
        (AFISAFI_VPNV6_MULTICAST, 'VPNv6 Multicast'),
        (AFISAFI_VPNV6_FLOWSPEC, 'VPNv6 Flowspec')
    ]


class IPAddressFamilyChoices(ChoiceSet):

    FAMILY_4 = 'ipv4'
    FAMILY_6 = 'ipv6'
    
    CHOICES = (
        (FAMILY_4, 'IPv4'),
        (FAMILY_6, 'IPv6'),
    )
