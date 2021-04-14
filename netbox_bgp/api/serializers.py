from rest_framework.serializers import ModelSerializer

from netbox.api import ChoiceField

from netbox_bgp.models import ASN, ASNStatusChoices, BGPSession, SessionStatusChoices


class ASNSerializer(ModelSerializer):
    status = ChoiceField(choices=ASNStatusChoices, required=False)

    class Meta:
        model = ASN
        fields = '__all__'


class BGPSessionSerializer(ModelSerializer):
    status = ChoiceField(choices=SessionStatusChoices, required=False)

    class Meta:
        model = BGPSession
        fields = '__all__'
