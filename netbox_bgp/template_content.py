from netbox.plugins import PluginTemplateExtension

from .models import BGPSession, Redistributing
from .tables import BGPSessionTable, RedistributingTable


class DeviceRelatedObjects(PluginTemplateExtension):
    models = ('dcim.device',)

    def full_width_page(self):
        obj = self.context['object']
        sess = BGPSession.objects.filter(device=obj)
        sess_table = BGPSessionTable(sess)
        redistributing = Redistributing.objects.filter(device=obj)
        redistributing_table = RedistributingTable(redistributing)
        return self.render(
            'netbox_bgp/device_extend.html',
            extra_context={
                'related_session_table': sess_table,
                'related_redistributing_table': redistributing_table
            }
        )

template_extensions = [DeviceRelatedObjects]
