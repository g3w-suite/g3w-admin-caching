from django.template import loader, Context
from django.dispatch import receiver
from core.signals import load_layer_actions
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