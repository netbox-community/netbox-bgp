import strawberry

from netbox_bgp.choices import (
    CommunityStatusChoices,
    SessionStatusChoices,
    ActionChoices,
    IPAddressFamilyChoices,
)

__all__ = (
    "NetBoxBGPCommunityStatusEnum",
    "NetBoxBGPSessionStatusEnum",
    "NetBoxBGPActionEnum",
    "NetBoxBGPIPAddressFamilyEnum",
)

NetBoxBGPCommunityStatusEnum = strawberry.enum(CommunityStatusChoices.as_enum())
NetBoxBGPSessionStatusEnum = strawberry.enum(SessionStatusChoices.as_enum())
NetBoxBGPActionEnum = strawberry.enum(ActionChoices.as_enum())
NetBoxBGPIPAddressFamilyEnum = strawberry.enum(IPAddressFamilyChoices.as_enum())

