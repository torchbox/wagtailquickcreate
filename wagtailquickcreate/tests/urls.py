from django.contrib import admin
from django.urls import include, path

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

private_urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
]

# Public URLs that are meant to be cached.
urlpatterns = []

urlpatterns = private_urlpatterns + urlpatterns + [
    # Add Wagtail URLs at the end.
    # Wagtail cache-control is set on the page models's serve methods.
    path('', include(wagtail_urls)),
]
