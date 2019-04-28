from wagtail.tests.utils import WagtailTestUtils
from wagtail.core.models import Page
from django.conf import settings
from django.test import TestCase
from wagtailquickcreate.tests.standardpages.models import IndexPage
from django.urls import reverse
from django.contrib.auth import get_user_model


class WagtailQuickCreateTests(TestCase, WagtailTestUtils):
    fixtures = ['wagtailquickcreate/tests/fixtures/test.json']

    def setUp(self):
        super().setUp()
        self.login()
        self.home = Page.objects.get(pk=2)
        self.index = IndexPage(
            title='Section 1',
            slug='section-1',
            introduction='...'
        )
        self.index_2 = IndexPage(
            title='Section 2',
            slug='section-2',
            introduction='...'
        )
        self.home.add_child(instance=self.index)
        self.index.add_child(instance=self.index_2)

    def test_admin(self):
        response = self.client.get(reverse('wagtailadmin_home'))
        self.assertEqual(response.status_code, 200)

    def test_quickcreate_panel_links(self):
        response = self.client.get('/admin/')
        self.assertContains(response, 'Add Image', html=True)
        self.assertContains(response, 'Add Document', html=True)
        self.assertContains(response, 'Add Information page', html=True)

    def test_first_level_index_page_in_shortcut_view(self):
        response = self.client.get('/admin/quickcreate/create/standardpages/informationpage/')
        self.assertContains(response, 'Home > <strong>Section 1</strong>', html=True)

    def test_second_level_index_in_shortcut_view(self):
        response = self.client.get('/admin/quickcreate/create/standardpages/informationpage/')
        self.assertContains(response, 'Home > Section 1 > <strong>Section 2</strong>', html=True)
