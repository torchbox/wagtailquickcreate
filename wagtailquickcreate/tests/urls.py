
import wagtail.core.urls
import wagtail.admin.urls
from django.conf.urls import include, url

urlpatterns = [
    url(r'^admin/', include(wagtail.admin.urls)),
    url(r'', include(wagtail.core.urls)),
]