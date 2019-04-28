
import wagtail.core.urls
import wagtail.admin.urls
from django.conf.urls import include, url
from django.urls import include, path
from django.contrib import admin
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from django.conf import settings
from wagtail.core import urls as wagtail_urls

from wagtail.utils.urlpatterns import decorate_urlpatterns


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
