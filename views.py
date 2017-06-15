# -*- coding: utf-8 -*-
from django.apps import apps
from django.views.generic import FormView
from core.mixins.views import AjaxableFormResponseMixin, G3WRequestViewMixin, G3WProjectViewMixin
from .forms import ActiveCachingLayerForm
from .models import G3WCachingLayer


class ActiveCaqchingLayerView(AjaxableFormResponseMixin, G3WProjectViewMixin, G3WRequestViewMixin, FormView):
    """
    View for enabled caching layer form
    """

    form_class = ActiveCachingLayerForm
    template_name = 'editing/editing_layer_active_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.layer_id = kwargs['layer_id']
        return super(ActiveCaqchingLayerView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return None

    def get_form_kwargs(self):

        kwargs = super(ActiveCaqchingLayerView, self).get_form_kwargs()

        # get model by app
        Layer = apps.get_app_config(self.app_name).get_model('layer')
        self.layer = Layer.objects.get(pk=self.layer_id)

        # try to find notes config
        try:
            self.activated = G3WCachingLayer.objects.get(app_name=self.app_name, layer_id=self.layer_id)
            kwargs['initial']['active'] = True
        except:
            self.activated = None
            kwargs['initial']['active'] = False

        return kwargs

    def form_valid(self, form):

        if form.cleaned_data['active']:
            if not self.activated:
                G3WCachingLayer.objects.create(app_name=self.app_name, layer_id=self.layer_id)
        else:
            if self.activated:
                self.activated.delete()
        return super(ActiveCaqchingLayerView, self).form_valid(form)
