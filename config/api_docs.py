from django.conf.urls import url
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Приложение опросов: REST API",
        default_version='v1',
        description="Описание методов для работы с опросами",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0)),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='swagger'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),
]
