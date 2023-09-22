from django.apps import apps
from django.conf import settings
from django.urls import path
from django.utils.safestring import mark_safe

from wagtail.admin.site_summary import SiteSummaryPanel, SummaryItem

from wagtail import hooks

from .views import QuickCreateView


class QuickCreatePanel(SummaryItem):
    template_name = "wagtailquickcreate/panel.html"
    order = 50

    def get_context_data(self, parent_context):
        context = super().get_context_data(parent_context)
        quick_create_page_types = getattr(
            settings, "WAGTAIL_QUICK_CREATE_PAGE_TYPES", []
        )

        if not quick_create_page_types:
            return ""

        # Make a list of the models with edit links
        # EG [{'link': 'news/NewsPage', 'name': 'News page'}]
        page_models = []
        for i in quick_create_page_types:
            item = {}
            # When testing, or if the app/model has a specific name
            # target the last 2 list values
            i = i.split(".")
            i = ".".join(i[-2:])
            model = apps.get_model(i)
            item["link"] = model._meta.app_label + "/" + model.__name__
            item["name"] = model.get_verbose_name()
            page_models.append(item)

        # Build up an html chunk for the links to be rendered in the panel
        page_models_html_chunk = []
        for item in page_models:
            model = apps.get_model(item["link"].replace("/", "."))

            # Si le modèle a un seul type de parent, trouvez ce parent
            # et générer un lien direct pour la création.
            if len(model.parent_page_types) == 1:
                parent_model = apps.get_model(model.parent_page_types[0])
                parent_instance = (
                    parent_model.objects.first()
                )  # ou autre logique pour obtenir l'instance parente correcte
                if parent_instance:
                    model_name_lower = model.__name__.lower()
                    link = f"/admin/pages/add/{model._meta.app_label}/{model_name_lower}/{parent_instance.id}/"
                    page_models_html_chunk.append(
                        f'<a href="{link}"><button class="button bicolor button--icon margin-bottom-sm" style="margin-right:6px;margin-bottom:6px;">'
                        f'<span class="icon-wrapper"><svg class="icon icon-plus icon" aria-hidden="true">'
                        f'<use href="#icon-plus"></use></svg></span>Add {item["name"]}</button></a>'
                    )
                else:
                    # Si aucun parent n'est trouvé, vous pouvez soit ignorer le bouton, soit utiliser la logique actuelle.
                    pass
            else:
                page_models_html_chunk.append(
                    """
                    <a href="/admin/quickcreate/create/{model_link}/">
                    <button class="button bicolor button--icon margin-bottom-sm" style="margin-right:6px;margin-bottom:6px;">
                    <span class="icon-wrapper">
                    <svg class="icon icon-plus icon" aria-hidden="true"><use href="#icon-plus"></use></svg>
                    </span>
                    Add {model_name}</button></a>""".format(
                        model_link=item["link"], model_name=item["name"]
                    )
                )

        page_models_html_chunk = list(set(page_models_html_chunk))

        if getattr(settings, "WAGTAIL_QUICK_CREATE_IMAGES", False):
            page_models_html_chunk.append(
                """
                    <a href="/admin/images/multiple/add/">
                    <button class="button bicolor button--icon" style="margin-right:6px;margin-bottom:6px;">
                    <span class="icon-wrapper">
                    <svg class="icon icon-plus icon" aria-hidden="true"><use href="#icon-plus"></use></svg>
                    </span>
                    Add Image</button></a>
                    """
            )
        if getattr(settings, "WAGTAIL_QUICK_CREATE_DOCUMENTS", False):
            page_models_html_chunk.append(
                """
                    <a href="/admin/documents/multiple/add/">
                    <button class="button bicolor button--icon" style="margin-right:6px;margin-bottom:6px;">
                    <span class="icon-wrapper">
                    <svg class="icon icon-plus icon" aria-hidden="true"><use href="#icon-plus"></use></svg>
                    </span>
                    Add Document</button></a>
                    """
            )
        context["models"] = mark_safe("".join(page_models_html_chunk))
        return context


@hooks.register("register_admin_urls")
def urlconf_time():
    # Example: http://127.0.0.1:8000/admin/quickcreate/create/standardpages/InformationPage/
    return [
        path("quickcreate/create/<str:app>/<str:model>/", QuickCreateView.as_view()),
    ]


@hooks.register("construct_homepage_panels")
def add_quick_create_panel(request, panels):
    # Replace the site summary panel with our custom panel
    if getattr(settings, "WAGTAIL_QUICK_CREATE_REPLACE_SUMMARY_PANEL", False):
        for i, v in enumerate(panels):
            if isinstance(v, SiteSummaryPanel):
                panels[i] = QuickCreatePanel(request)
    else:
        panels.append(QuickCreatePanel(request))
    return panels
