from utilities.choices import ChoiceSet


class ASNStatusChoices(ChoiceSet):

    STATUS_ACTIVE = 'active'
    STATUS_RESERVED = 'reserved'
    STATUS_DEPRECATED = 'deprecated'

    CHOICES = (
        (STATUS_ACTIVE, 'Active', 'blue'),
        (STATUS_RESERVED, 'Reserved', 'cyan'),
        (STATUS_DEPRECATED, 'Deprecated', 'red'),
    )


class SessionStatusChoices(ChoiceSet):

    STATUS_OFFLINE = 'offline'
    STATUS_ACTIVE = 'active'
    STATUS_PLANNED = 'planned'
    STATUS_FAILED = 'failed'

    CHOICES = (
        (STATUS_OFFLINE, 'Offline', 'orange'),
        (STATUS_ACTIVE, 'Active', 'green'),
        (STATUS_PLANNED, 'Planned', 'cyan'),
        (STATUS_FAILED, 'Failed', 'red'),
    )


class ActionChoices(ChoiceSet):

    CHOICES = [
        ('permit', 'Permit', 'green'),
        ('deny', 'Deny', 'red'),
    ]


class AFISAFIChoices(ChoiceSet):
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

    CHOICES = (

    )


class IPAddressFamilyChoices(ChoiceSet):

    FAMILY_4 = 4
    FAMILY_6 = 6

    CHOICES = (
        (FAMILY_4, 'IPv4'),
        (FAMILY_6, 'IPv6'),
    )
