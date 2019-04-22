import importlib
from django.conf import settings
from django.apps import apps

from django.views.generic import TemplateView
from django.shortcuts import redirect
from wagtail.core.models import UserPagePermissionsProxy


# Helper function to work out page permissions
def filter_pages_by_permission(user, pages):
    user_permissions = UserPagePermissionsProxy(user)
    return [
        page for page in pages
        if user_permissions.for_page(page).can_add_subpage()
    ]


class QuickCreateView(TemplateView):
    template_name = "wagtailquickcreate/create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Work out the parent pages to offer to the user to add
        # their new page under, for this we need to query the objects/models
        # allowed parent pages
        _model = kwargs.pop('model')
        app = kwargs.pop('app')
        model = apps.get_model(app, _model)
        parent_models = model.allowed_parent_page_models()

        # With the 'allowed parent page' models we have found, get all
        # those objects from the database so we can offer them as parent pages
        # for the new child page being added
        self.pages = []
        for pm in parent_models:
            for object in pm.objects.all():
                self.pages.append(object)

        # Check the current user has permission to edit pages in question
        self.pages = filter_pages_by_permission(self.request.user, self.pages)

        parent_pages = []
        for i in self.pages:
            item = {}
            item['id'] = i.id
            item['title'] = i.title
            item['app_label'] = i._meta.app_label
            item['model'] = _model
            item['page'] = i
            # Also send through the section page ancestors for a clearer link path
            # to the user.
            item['ancestors'] = i.get_ancestors()
            parent_pages.append(item)

        context['model_verbose_name'] = model.get_verbose_name()
        context['parent_pages'] = parent_pages
        return context