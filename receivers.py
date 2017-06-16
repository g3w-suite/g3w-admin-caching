from django.template import loader, Context
from django.dispatch import receiver
from core.signals import load_layer_actions, after_serialized_project_layer
from caching.models import G3WCachingLayer

@receiver(load_layer_actions)
def editingLayerAction(sender, **kwargs):
    """
    Return html actions editing for project layer.
    """

    # only admin and editor1 or editor2:
    if sender.has_perm('change_project', kwargs['layer'].project):

        # add if is active
        try:
            G3WCachingLayer.objects.get(app_name=kwargs['app_name'], layer_id=kwargs['layer'].pk)
            kwargs['active'] = True
        except:
            kwargs['active'] = False

        template = loader.get_template('caching/layer_action.html')
        return template.render(Context(kwargs))


@receiver(after_serialized_project_layer)
def add_caching_urs(sender, **kwargs):
    """
    Receiver to ad rcaching data and url.
    """
    layer = kwargs['layer']
    data = {
        'operation_type': 'update',
        'values': {},
    }

    # get config if exists:
    caching_layers = {str(cl): cl for cl in G3WCachingLayer.objects.all()}
    layer_key_name = "{}{}".format(layer._meta.app_label, layer.pk)
    if layer_key_name in caching_layers.keys():
        data['values'] = {'cache_url': '/caching/api/{}'.format(layer_key_name)}
    return data