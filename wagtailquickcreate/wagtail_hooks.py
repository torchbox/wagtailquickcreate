from django.conf.urls import url
from django.utils.safestring import mark_safe
from django.conf import settings
from django.apps import apps

from wagtail.admin.site_summary import SiteSummaryPanel
from wagtail.core import hooks

from .views import QuickCreateView


class QuickCreatePanel:
    order = 50

    def render(self):
        # Make a list of the models with edit links
        # EG [{'link': 'news/NewsPage', 'name': 'News page'}]
        page_models = []
        for i in settings.WAGTAIL_QUICK_CREATE_PAGE_TYPES:
            item = {}
            model = apps.get_model(i)
            item['link'] = model._meta.app_label + '/' + model.__name__
            item['name'] = model.get_verbose_name()
            page_models.append(item)

        # Build up an html chunk for the links to be rendered in the panel
        page_models_html_chunk = []

        for i in page_models:
            page_models_html_chunk.append("""
                <a href="/admin/quickcreate/create/{model_link}/"><button class="button bicolor icon icon-plus">Add {model_name}</button></a>""".format(model_link=i['link'], model_name=i['name']))

        page_models_html_chunk = list(set(page_models_html_chunk))

        if settings.WAGTAIL_QUICK_CREATE_IMAGES:
            page_models_html_chunk.append("""
            <a href="/admin/images/multiple/add/"><button class="button bicolor icon icon-plus">Add Image</button></a>
            """)
        if settings.WAGTAIL_QUICK_CREATE_DOCUMENTS:
            page_models_html_chunk.append("""
            <a href="/admin/documents/multiple/add/"><button class="button bicolor icon icon-plus">Add Document</button></a>
            """)

        return mark_safe("""
            <section class="panel wagtail_quick_create summary nice-padding">
            {models}</section>""".format(models=''.join(page_models_html_chunk)))


@hooks.register('register_admin_urls')
def urlconf_time():
    return [
        url(r'^quickcreate/create/(?P<app>\D+)/(?P<model>\D+)/', QuickCreateView.as_view()),
    ]


@hooks.register('construct_homepage_panels')
def add_quick_create_panel(request, panels):
    # Replace the site summary panel with our custom panel
    if settings.WAGTAIL_QUICK_CREATE_REPLACE_SUMMARY_PANEL:
        for i, v in enumerate(panels):
            if isinstance(v, SiteSummaryPanel):
                panels[i] = QuickCreatePanel()
    else:
        panels.append(QuickCreatePanel)
    return panels

