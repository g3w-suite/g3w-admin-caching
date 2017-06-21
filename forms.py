from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import HTML, Div
from core.mixins.forms import G3WRequestFormMixin, G3WProjectFormMixin


class ActiveCachingLayerForm(G3WRequestFormMixin, G3WProjectFormMixin, forms.Form):

    active = forms.BooleanField(label=_('Active'), required=False)
    reset_layer_cache_url = forms.CharField(required=False, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):

        super(ActiveCachingLayerForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                HTML(_('Check on uncheck to attive/desctive caching layer capabilities:')),
                Div(
                    Div(
                        'active',
                        'reset_layer_cache_url',
                        css_class='col-md-3'
                    ),
                    Div(
                        HTML("<a id='restcache' style='margin-top: 8px;' href='#' class='btn btn-sm btn-success'><i class='fa fa-eraser'></i> {}</a>"
                             .format(_('Reset cache'))),
                        css_class='col-md-9'
                    ),

                    css_class='row'
                ),

                css_class='col-md-12'
            )
        )