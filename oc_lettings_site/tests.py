from django.test import Client, TestCase
from django.urls import reverse, resolve
from pytest_django.asserts import assertTemplateUsed


class IndexTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_view_index(self):
        response = self.client.get(reverse('index'))
        content = response.content.decode()
        expected_content = '<title>Holiday Homes</title>'

        assert expected_content in content
        assert response.status_code == 200
        assertTemplateUsed(response, 'index.html')

    def test_url_index(self):
        path = reverse('index')
        assert path == '/'
        assert resolve(path).view_name == 'index'
