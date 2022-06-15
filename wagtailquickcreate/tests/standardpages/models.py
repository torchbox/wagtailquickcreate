from django.db import models

from wagtail import VERSION as WAGTAIL_VERSION

if WAGTAIL_VERSION >= (3, 0):
    from wagtail.models import Page
else:
    from wagtail.core.models import Page


class InformationPage(Page):
    parent_page_types = ['standardpages.IndexPage']

    introduction = models.TextField(blank=True)


class IndexPage(Page):

    introduction = models.TextField(blank=True)
