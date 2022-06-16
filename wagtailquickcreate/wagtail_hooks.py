from django.apps import apps
from django.conf import settings
from django.urls import path
from django.utils.safestring import mark_safe

from wagtail.admin.site_summary import SiteSummaryPanel, SummaryItem
from wagtail import VERSION as WAGTAIL_VERSION

if WAGTAIL_VERSION >= (3, 0):
    from wagtail import hooks
else:
    from wagtail.core import hooks

from .views import QuickCreateView


class QuickCreatePanel(SummaryItem):
    template_name = "wagtailquickcreate/panel.html"
    order = 50

    def get_context_data(self, parent_context):
        context = super().get_context_data(parent_context)
        quick_create_page_types = getattr(settings, "WAGTAIL_QUICK_CREATE_PAGE_TYPES", [])

        if not quick_create_page_types:
            return ""

        # Make a list of the models with edit links
        # EG [{'link': 'news/NewsPage', 'name': 'News page'}]
        page_models = []
        for i in quick_create_page_types:
            item = {}
            # When testing, or if the app/model has a specific name
            # target the last 2 list values
            i = i.split('.')
            i = '.'.join(i[-2:])
            model = apps.get_model(i)
            item['link'] = model._meta.app_label + '/' + model.__name__
            item['name'] = model.get_verbose_name()
            page_models.append(item)

        # Build up an html chunk for the links to be rendered in the panel
        page_models_html_chunk = [
            """
                <a href="/admin/quickcreate/create/{model_link}/">
                <button class="button bicolor icon icon-plus">Add {model_name}</button></a>""".format(
                model_link=i['link'], model_name=i['name']
            )
            for i in page_models
        ]

        page_models_html_chunk = list(set(page_models_html_chunk))

        if getattr(settings, "WAGTAIL_QUICK_CREATE_IMAGES", False):
            page_models_html_chunk.append("""
                    <a href="/admin/images/multiple/add/"><button class="button bicolor icon icon-plus">Add Image</button></a>
                    """)
        if getattr(settings, "WAGTAIL_QUICK_CREATE_DOCUMENTS", False):
            page_models_html_chunk.append("""
                    <a href="/admin/documents/multiple/add/"><button class="button bicolor icon icon-plus">
                    Add Document</button></a>
                    """)
        context["models"] = mark_safe(''.join(page_models_html_chunk))
        return context


@hooks.register('register_admin_urls')
def urlconf_time():
    # Example: http://127.0.0.1:8000/admin/quickcreate/create/standardpages/InformationPage/
    return [
        path('quickcreate/create/<str:app>/<str:model>/',
            QuickCreateView.as_view()),
    ]


@hooks.register('construct_homepage_panels')
def add_quick_create_panel(request, panels):
    # Replace the site summary panel with our custom panel
    if getattr(settings, "WAGTAIL_QUICK_CREATE_REPLACE_SUMMARY_PANEL", False):
        for i, v in enumerate(panels):
            if isinstance(v, SiteSummaryPanel):
                panels[i] = QuickCreatePanel(request)
    else:
        panels.append(QuickCreatePanel(request))
    return panels
