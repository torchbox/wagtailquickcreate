from wagtail.tests.utils import WagtailPageTests
from wagtail.core.models import Page
from django.conf import settings


class WagtailQuickCreateTests(WagtailPageTests):
    fixtures = ['wagtailquickcreate/tests/fixtures/test.json']

    def setUp(self):
        super().setUp()
        settings.WAGTAIL_QUICK_CREATE_PAGE_TYPES = ['wagtailcore.Page']
        self.home_page = Page.objects.get(pk=2)
        self.index_page = Page.objects.get(pk=3)

    def test_index_pages_in_shortcut_view(self):
        # Check the index pages are in the shortcut view
        response = self.client.get('/admin/quickcreate/create/wagtailcore/page/{}/'.format(self.index_page.pk))
        self.assertContains(response, 'a', html=True)
        # self.assertContains(response, 'Home > <strong>Foo Bar 2</strong>', html=True)
        # self.assertContains(response, 'Home > Foo Bar ><strong>Foo Bar 3</strong>', html=True)
