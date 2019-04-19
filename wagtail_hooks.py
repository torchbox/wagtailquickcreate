from django.conf.urls import url
from django.utils.safestring import mark_safe
from django.conf import settings
from django.apps import apps
from wagtail.admin.site_summary import SiteSummaryPanel

from wagtail.core import hooks

from .views import CreatePageShortcutView


class WelcomePanel:
    order = 50

    def render(self):
        # Make a list of the models with there edit links
        page_models = []
        page_models_html_chunk = []
        for i in settings.WAGTAIL_QUICK_CREATE_PAGE_TYPES:
            item = {}
            model = apps.get_model(i)
            item['link'] = model._meta.app_label + '/' + model.__name__
            item['name'] = model.get_verbose_name()
            page_models.append(item)

        for i in page_models:
            page_models_html_chunk.append("""
                <a href="/admin/quickcreate/create/{model_link}/"><button class="button bicolor icon icon-plus">Create {model_name}</button></a>""".format(model_link=i['link'], model_name=i['name']))

        page_models_html_chunk = list(set(page_models_html_chunk))

        return mark_safe("""
            <section class="panel wagtail_quick_create summary nice-padding">
            <h2>Quick Create</h2>
            {models}</section>""".format(models=''.join(page_models_html_chunk)))


@hooks.register('register_admin_urls')
def urlconf_time():
    return [
        url(r'^quickcreate/create/(?P<app>\D+)/(?P<model>\D+)/', CreatePageShortcutView.as_view()),
    ]


@hooks.register('construct_homepage_panels')
def add_another_welcome_panel(request, panels):
    # Replace the site summary panel with our custom panel
    if settings.WAGTAIL_QUICK_CREATE_REPLACE_SUMMARY_PANEL:
        for i, v in enumerate(panels):
            if isinstance(v, SiteSummaryPanel):
                panels[i] = WelcomePanel()
    else:
        panels.append(WelcomePanel)
    return panels
