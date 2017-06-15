from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import HTML
from core.mixins.forms import G3WRequestFormMixin, G3WProjectFormMixin


class ActiveCachingLayerForm(G3WRequestFormMixin, G3WProjectFormMixin, forms.Form):

    active = forms.BooleanField(label=_('Active'), required=False)

    def __init__(self, *args, **kwargs):

        super(ActiveCachingLayerForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            HTML(_('Check on uncheck to attive/desctive caching layer capabilities:')),
            'active',
        )