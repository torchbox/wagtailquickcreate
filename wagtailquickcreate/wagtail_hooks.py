from django.apps import apps
from django.conf import settings
from django.urls import path, reverse

from wagtail import hooks
from wagtail.admin.panels import Component

from .views import QuickCreateView


class QuickCreatePanel(Component):
    template_name = "wagtailquickcreate/panel.html"
    order = 50

    @property
    def initial_collpased(self):
        aria_expanded = "false"
        hidden = None
        if getattr(settings, "WAGTAIL_QUICK_CREATE_INITIAL_COLLAPSED", False):
            aria_expanded = "false"
            hidden = "until-found"
        else:
            aria_expanded = "true"
        return {"aria_expanded": aria_expanded, "hidden": hidden}

    def get_context_data(self, parent_context):
        context = super().get_context_data(parent_context)
        quick_create_page_types = getattr(
            settings, "WAGTAIL_QUICK_CREATE_PAGE_TYPES", []
        )

        if not quick_create_page_types:
            return ""

        # Make a list of the models with edit links
        # EG [{'link': 'news/NewsPage', 'name': 'News page'}]
        model_buttons = []
        model_button_errors = []
        for page_type in quick_create_page_types:
            # When testing, or if the app/model has a specific name
            # target the last 2 list values
            page_type = page_type.split(".")
            page_type = ".".join(page_type[-2:])
            try:
                # Try to get the model, if it fails, add it to the errors list
                # This can happen if the model listed in WAGTAIL_QUICK_CREATE_PAGE_TYPES
                # is not a valid model die to a typo of the model name has changed or it's been removed
                model = apps.get_model(page_type)
                model_buttons.append(
                    {
                        "link": f"/admin/quickcreate/create/{model._meta.app_label}/{model.__name__}/",
                        "name": model.get_verbose_name(),
                    }
                )
            except LookupError:
                model_button_errors.append(page_type)

        if getattr(settings, "WAGTAIL_QUICK_CREATE_IMAGES", False):
            model_buttons.append(
                {"link": reverse("wagtailimages:index"), "name": "Image"}
            )

        if getattr(settings, "WAGTAIL_QUICK_CREATE_DOCUMENTS", False):
            model_buttons.append(
                {"link": reverse("wagtaildocs:index"), "name": "Document"}
            )

        context["initial_collapsed"] = self.initial_collpased
        context["model_buttons"] = model_buttons
        context["model_button_errors"] = model_button_errors
        return context


@hooks.register("register_admin_urls")
def urlconf_time():
    # Example: http://127.0.0.1:8000/admin/quickcreate/create/standardpages/InformationPage/
    return [
        path("quickcreate/create/<str:app>/<str:model>/", QuickCreateView.as_view()),
    ]


@hooks.register("construct_homepage_panels")
def add_quick_create_panel(request, panels):
    panels.append(QuickCreatePanel())
    return panels
