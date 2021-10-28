from django import forms
from utilities.forms import DynamicModelMultipleChoiceField, DynamicModelChoiceField
from django.urls import reverse
from django.forms import BoundField


class PluginDynamicModelChoiceField(DynamicModelChoiceField):
    def get_bound_field(self, form, field_name):
        """Override the parent method to work with plugins.
        
        The changes from upstream are:
          1. The data_url was changed to reference the plugin uri path
          2. The `if data` conditional was removed from the queryset lookup so that the
             field can be populated.. am I missing something on this one? It seems like
             there should be a way around this.
        """
        bound_field = BoundField(form, self, field_name)

        # Set initial value based on prescribed child fields (if not already set)
        if not self.initial and self.initial_params:
            filter_kwargs = {}
            for kwarg, child_field in self.initial_params.items():
                value = form.initial.get(child_field.lstrip('$'))
                if value:
                    filter_kwargs[kwarg] = value
            if filter_kwargs:
                self.initial = self.queryset.filter(**filter_kwargs).first()

        # Modify the QuerySet of the field before we return it. Limit choices to any data already bound: Options
        # will be populated on-demand via the APISelect widget.
        data = bound_field.value()
        field_name = getattr(self, 'to_field_name') or 'pk'
        filter = self.filter(field_name=field_name)
        try:
            self.queryset = filter.filter(self.queryset, data)
        except (TypeError, ValueError):
            # Catch any error caused by invalid initial data passed from the user
            self.queryset = self.queryset.none()

        # Set the data URL on the APISelect widget (if not already set)
        widget = bound_field.field.widget
        if not widget.attrs.get('data-url'):
            app_label = self.queryset.model._meta.app_label
            model_name = self.queryset.model._meta.model_name
            data_url = reverse(
                "plugins-api:{}-api:{}-list".format(app_label, model_name)
            )
            widget.attrs['data-url'] = data_url

        return bound_field

class PluginDynamicModelMultipleChoiceField(DynamicModelMultipleChoiceField):
    def get_bound_field(self, form, field_name):
        """Override the parent method to work with plugins.
        
        The changes from upstream are:
          1. The data_url was changed to reference the plugin uri path
          2. The `if data` conditional was removed from the queryset lookup so that the
             field can be populated.. am I missing something on this one? It seems like
             there should be a way around this.
        """
        bound_field = BoundField(form, self, field_name)

        # Set initial value based on prescribed child fields (if not already set)
        if not self.initial and self.initial_params:
            filter_kwargs = {}
            for kwarg, child_field in self.initial_params.items():
                value = form.initial.get(child_field.lstrip('$'))
                if value:
                    filter_kwargs[kwarg] = value
            if filter_kwargs:
                self.initial = self.queryset.filter(**filter_kwargs).first()

        # Modify the QuerySet of the field before we return it. Limit choices to any data already bound: Options
        # will be populated on-demand via the APISelect widget.
        data = bound_field.value()
        field_name = getattr(self, 'to_field_name') or 'pk'
        filter = self.filter(field_name=field_name)
        try:
            self.queryset = filter.filter(self.queryset, data)
        except (TypeError, ValueError):
            # Catch any error caused by invalid initial data passed from the user
            self.queryset = self.queryset.none()

        # Set the data URL on the APISelect widget (if not already set)
        widget = bound_field.field.widget
        if not widget.attrs.get('data-url'):
            app_label = self.queryset.model._meta.app_label
            model_name = self.queryset.model._meta.model_name
            data_url = reverse(
                "plugins-api:{}-api:{}-list".format(app_label, model_name)
            )
            widget.attrs['data-url'] = data_url

        return bound_field


class SelectWithDisabled(forms.Select):
    """
    Modified the stock Select widget to accept choices using a dict() for a label. The dict for each option must include
    'label' (string) and 'disabled' (boolean).
    """
    option_template_name = 'widgets/selectwithdisabled_option.html'


class StaticSelect2(SelectWithDisabled):
    """
    A static <select> form widget using the Select2 library.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.attrs['class'] = 'netbox-select2-static'


class StaticSelect2Multiple(StaticSelect2, forms.SelectMultiple):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.attrs['data-multiple'] = 1