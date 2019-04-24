import wagtail_factories
from wagtail.tests.utils import WagtailPageTests
from wagtail.core.models import Page
from django.conf import settings

class IndexPageFactory(wagtail_factories.PageFactory):

    class Meta:
        model = Page


class WagtailQuickCreateTests(WagtailPageTests):
    def setUp(self):
        super().setUp()
        settings.WAGTAIL_QUICK_CREATE_PAGE_TYPES = ['wagtailcore.Page']
        self.home_page = Page.objects.get(pk=3)
        self.index_page = IndexPageFactory(
            slug='foobar',
            title='Foo Bar',
            parent=self.home_page
        )
        self.index_page_2 = IndexPageFactory(
            slug='foobar-2',
            title='Foo Bar 2',
            parent=self.home_page
        )
        self.index_page_3 = IndexPageFactory(
            slug='foobar-3',
            title='Foo Bar 3',
            parent=self.index_page
        )

    def test_index_pages_in_shortcut_view(self):
        # Check the index pages are in the shortcut view
        response = self.client.get('/admin/quickcreate/create/wagtailcore/page/{}/'.format(self.index_page.pk))
        self.assertContains(response, 'Home > <strong>Foo Bar</strong>', html=True)
        self.assertContains(response, 'Home > <strong>Foo Bar 2</strong>', html=True)
        self.assertContains(response, 'Home > Foo Bar ><strong>Foo Bar 3</strong>', html=True)
