from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import TileStacheTileApiView


urlpatterns = [
    url(r'^api/(?P<layer_name>[-\w]+)/(?P<z>\d+)/(?P<x>\d+)/(?P<y>\d+).(?P<extension>\w+)/$',
        login_required(TileStacheTileApiView.as_view()), name='caching-api-tile')
]
