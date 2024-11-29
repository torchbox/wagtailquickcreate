from bs4 import BeautifulSoup

from django.test import TestCase
from django.urls import reverse

from wagtail.models import Page
from wagtail.test.utils import WagtailTestUtils

from wagtailquickcreate.tests.standardpages.models import IndexPage


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
        soup = BeautifulSoup(response.content, 'html.parser')
        quick_create_content = soup.find('div', id='quickcreate-content')
        buttons = quick_create_content.find_all('a')
        self.assertTrue(len(buttons) == 3)
        self.assertTrue(buttons[0].text.strip() == 'Information page')
        self.assertTrue(buttons[0]['href'] == '/admin/quickcreate/create/standardpages/InformationPage/')
        self.assertTrue(buttons[1].text.strip() == 'Image')
        self.assertTrue(buttons[1]['href'] == '/admin/images/')
        self.assertTrue(buttons[2].text.strip() == 'Document')
        self.assertTrue(buttons[2]['href'] == '/admin/documents/')

    def test_quickcreate_index_page_title(self):
        response = self.client.get('/admin/quickcreate/create/standardpages/informationpage/')
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('h1')
        self.assertTrue(title.text.strip() == 'Add Information page')

    def test_first_level_index_page_in_shortcut_view(self):
        response = self.client.get('/admin/quickcreate/create/standardpages/informationpage/')
        soup = BeautifulSoup(response.content, 'html.parser')
        parent_link = soup.find('a', href='/admin/pages/add/standardpages/informationpage/3/')
        self.assertIsNotNone(parent_link)
        self.assertTrue(parent_link.text.replace('\n', ''), 'Home > <strong>Section 1</strong>')

    def test_second_level_index_in_shortcut_view(self):
        response = self.client.get('/admin/quickcreate/create/standardpages/informationpage/')
        soup = BeautifulSoup(response.content, 'html.parser')
        parent_link = soup.find('a', href='/admin/pages/add/standardpages/informationpage/4/')
        self.assertIsNotNone(parent_link)
        self.assertTrue(parent_link.text.replace('\n', ''), 'Home > Section 1 > <strong>Section 2</strong>')
