from django.test import TestCase
from django.urls import reverse

from wagtail.models import Page
from wagtail.test.utils import WagtailTestUtils

from wagtailquickcreate.tests.standardpages.models import IndexPage


class WagtailQuickCreateTests(TestCase, WagtailTestUtils):
    fixtures = ["wagtailquickcreate/tests/fixtures/test.json"]

    def setUp(self):
        super().setUp()
        self.login()
        self.home = Page.objects.get(pk=2)
        self.index = IndexPage(title="Section 1", slug="section-1", introduction="...")
        self.index_2 = IndexPage(
            title="Section 2", slug="section-2", introduction="..."
        )
        self.home.add_child(instance=self.index)
        self.index.add_child(instance=self.index_2)

    def test_admin(self):
        response = self.client.get(reverse("wagtailadmin_home"))
        self.assertEqual(response.status_code, 200)

    def test_quickcreate_panel_links(self):
        response = self.client.get("/admin/")
        self.assertTrue("Add Image" in str(response.content))
        self.assertTrue("Add Document" in str(response.content))
        self.assertTrue("Add Information page" in str(response.content))

    def test_first_level_index_page_in_shortcut_view(self):
        response = self.client.get(
            "/admin/quickcreate/create/standardpages/informationpage/"
        )
        self.assertContains(
            response,
            "Home >\n                            "
            "\n                        "
            "\n                        "
            "<strong>Section 1</strong>",
        )

    def test_second_level_index_in_shortcut_view(self):
        response = self.client.get(
            "/admin/quickcreate/create/standardpages/informationpage/"
        )
        self.assertContains(
            response,
            "Home >\n                            "
            "\n                        "
            "\n                            "
            "\n                                "
            "Section 1 >\n                            "
            "\n                        "
            "\n                        "
            "<strong>Section 2</strong>",
        )
