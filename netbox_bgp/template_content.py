from netbox.plugins import PluginTemplateExtension

class DeviceBGPSession(PluginTemplateExtension):
    models = ('dcim.device',)

    def left_page(self):
        if self.context['config'].get('device_ext_page') == 'left':
            return self.x_page()
        return ''

    def right_page(self):
        if self.context['config'].get('device_ext_page') == 'right':
            return self.x_page()
        return ''

    def full_width_page(self):
        if self.context['config'].get('device_ext_page') == 'full_width':
            return self.x_page()
        return ''

    def x_page(self):
        return self.render(
            'netbox_bgp/device_extend.html',
        )

template_extensions = [DeviceBGPSession]
