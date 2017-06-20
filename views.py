# -*- coding: utf-8 -*-
from django.apps import apps
from django.views.generic import FormView
from django.http import HttpResponse
from django.db import transaction
import TileStache
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from core.mixins.views import AjaxableFormResponseMixin, G3WRequestViewMixin, G3WProjectViewMixin
from .forms import ActiveCachingLayerForm
from .models import G3WCachingLayer
from .utils import get_config
from .api.permissions import TilePermission

class ActiveCachingLayerView(AjaxableFormResponseMixin, G3WProjectViewMixin, G3WRequestViewMixin, FormView):
    """
    View for enabled caching layer form
    """

    form_class = ActiveCachingLayerForm
    template_name = 'editing/editing_layer_active_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.layer_id = kwargs['layer_id']
        return super(ActiveCachingLayerView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return None

    def get_form_kwargs(self):

        kwargs = super(ActiveCachingLayerView, self).get_form_kwargs()

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

    @transaction.atomic
    def form_valid(self, form):

        tilestache_cfg = get_config()

        if form.cleaned_data['active']:
            if not self.activated:
                caching_layer = G3WCachingLayer.objects.create(app_name=self.app_name, layer_id=self.layer_id)
                tilestache_cfg.add_layer(str(caching_layer), caching_layer)
        else:
            if self.activated:
                tilestache_cfg.remove_layer(str(self.activated))
                self.activated.delete()

        return super(ActiveCachingLayerView, self).form_valid(form)


class TileStacheTileApiView(APIView):
    """
    renders tilestache tiles
    based on django-tilestache tilestache api view:
    https://gitlab.sigmageosistemas.com.br/dev/django-tilestache/blob/master/django_tilestache/views.py
    """

    permission_classes = (
        TilePermission,
    )

    def get(self, request, layer_name, z, x, y, extension):
        """
        Fetch tiles with tilestache.
        """

        try:
            extension = extension.upper()
            config = get_config().config
            path_info = "{}/{}/{}/{}.{}".format(layer_name, z, x, y, extension)
            coord, extension = TileStache.splitPathInfo(path_info)[1:]
            try:
                tilestache_layer = config.layers[layer_name]
            except:
                return Response({'status': 'layer not found'}, status=status.HTTP_404_NOT_FOUND)

            status_code, headers, content = tilestache_layer.getTileResponse(coord, extension)
            mimetype = headers.get('Content-Type')
            if len(content) == 0:
                status_code = 404

            response = HttpResponse(
                content,
                **{
                    'content_type': mimetype,
                    'status': status_code
                }
            )
            if hasattr(tilestache_layer, 'allowed origin'):
                response['Access-Control-Allow-Origin'] = tilestache_layer.get('allowed origin')
            return response
        except Exception as ex:
            return Response(
                {
                    'status': 'error',
                    'message': ex.message
                },
                status=status.HTTP_404_NOT_FOUND
            )
