from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title='DRF-API',
        default_version='v1',
        description="Do'kon uchun API",
        contact=openapi.Contact(
            email="azizillonabiyev52@gmail.com"
        )
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include('users.urls')),
    path('api/', include('products.urls')),

    path(
        'swagger/',
        schema_view.with_ui('swagger',cache_timeout=0),
        name='schema-view-api'
    ),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)