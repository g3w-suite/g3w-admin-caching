from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import ActiveCachingLayerView

urlpatterns = [
    url(r'^(?P<group_slug>[-_\w\d]+)/(?P<project_type>[-_\w\d]+)/(?P<project_slug>[-_\w\d]+)/(?P<layer_id>[0-9]+)/'
        r'active/$',
        login_required(ActiveCachingLayerView.as_view()), name='caching-layer-active'),
]
