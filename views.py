import importlib
from django.conf import settings
from django.apps import apps

from django.views.generic import TemplateView
from django.shortcuts import redirect
from wagtail.core.models import UserPagePermissionsProxy


def filter_pages_by_permission(user, pages):
    user_permissions = UserPagePermissionsProxy(user)
    return [
        page for page in pages
        if user_permissions.for_page(page).can_add_subpage()
    ]


class CreatePageShortcutView(TemplateView):
    template_name = "wagtail_quick_create/create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        _model = kwargs.pop('model')
        app = kwargs.pop('app')
        model = apps.get_model(app, _model)
        parent_model = model.allowed_parent_page_models()
        self.pages = []

        for pm in parent_model:
            # TODO queries Needs finessing, not sure how to do this
            for object in pm.objects.all():
                self.pages.append(object)
        self.pages = filter_pages_by_permission(self.request.user, self.pages)
        allowed_sections = []

        for i in self.pages:
            item = {}
            item['id'] = i.id
            item['title'] = i.title
            item['app_label'] = i._meta.app_label
            item['model'] = _model
            item['page'] = i
            item['ancestors'] = i.get_ancestors()
            allowed_sections.append(item)

        context['model_verbose_name'] = model.get_verbose_name()
        context['allowed'] = allowed_sections
        return context