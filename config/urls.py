from django.contrib import admin
from django.urls import include, path

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

from works.views import ContributorViewSet, WorkViewSet

router = routers.DefaultRouter()
router.register(r'contributors', ContributorViewSet)
router.register(r'works', WorkViewSet)

# TODO: fix issue with displaying wrong schema for response due to pagination
schema_view = get_schema_view(
   openapi.Info(title='Single Works View API', default_version='v1'),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/docs/', schema_view.with_ui('redoc', cache_timeout=0), name='api-docs'),
    path('api/', include((router.urls, 'api'), namespace='api'))
]
