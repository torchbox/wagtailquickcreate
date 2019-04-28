from django.conf import settings
from django.db import models
from wagtail.core.models import Page


class InformationPage(Page):
    parent_page_types = ['standardpages.IndexPage']

    introduction = models.TextField(blank=True)


class IndexPage(Page):

    introduction = models.TextField(blank=True)

