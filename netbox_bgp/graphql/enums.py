import strawberry

from netbox_bgp.choices import (
    CommunityStatusChoices,
    SessionStatusChoices,
    ActionChoices,
    IPAddressFamilyChoices,
    RedistributeSourceChoices,
)

__all__ = (
    "NetBoxBGPCommunityStatusEnum",
    "NetBoxBGPSessionStatusEnum",
    "NetBoxBGPActionEnum",
    "NetBoxBGPIPAddressFamilyEnum",
    "NetBoxBGPRedistributingRedistributeSourceEnum",
)

NetBoxBGPCommunityStatusEnum = strawberry.enum(CommunityStatusChoices.as_enum(), name="NetBoxBGPCommunityStatusEnum")
NetBoxBGPSessionStatusEnum = strawberry.enum(SessionStatusChoices.as_enum(), name="NetBoxBGPSessionStatusEnum")
NetBoxBGPActionEnum = strawberry.enum(ActionChoices.as_enum(), name="NetBoxBGPActionEnum")
NetBoxBGPIPAddressFamilyEnum = strawberry.enum(IPAddressFamilyChoices.as_enum(), name="NetBoxBGPIPAddressFamilyEnum")
NetBoxBGPRedistributingRedistributeSourceEnum = strawberry.enum(
    RedistributeSourceChoices.as_enum(),
    name="NetBoxBGPRedistributingRedistributeSourceEnum"
)
