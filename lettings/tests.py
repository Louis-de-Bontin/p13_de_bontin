from django.test import Client, TestCase
from django.urls import reverse, resolve
from pytest_django.asserts import assertTemplateUsed


from lettings.models import Address, Letting


class LettingTestCase(TestCase):
    """
    Test class for lettings app.
    """
    def setUp(self):
        Address.objects.create(
            number=1,
            street='Sukhumvit',
            city='Bang na',
            state='Bangkok',
            zip_code=10260,
            country_iso_code='TH'
        )
        Address.objects.create(
            number=20,
            street='Asoke',
            city='Bangkok',
            state='Bangkok',
            zip_code=10000,
            country_iso_code='TH'

        Letting.objects.create(
            title='Ideo Mobi',
            address=Address.objects.get(id=1)
        )
        Letting.objects.create(
            title='Exchange Tower',
            address=Address.objects.get(id=2)
        )

        self.client = Client()


class TestLettingView(LettingTestCase):
    def test_view_index(self):
        response = self.client.get(reverse('lettings_index'))
        content = response.content.decode()
        expected_title = '<title>Lettings</title>'
        expected_letting = 'Ideo Mobi'

        assert expected_title in content
        assert expected_letting in content
        assert response.status_code == 200
        assertTemplateUsed(response, 'lettings_index.html')

    def test_view_letting_should_return_letting(self):
        response = self.client.get(reverse('letting', kwargs={'letting_id': 2}))
        content = response.content.decode()
        expected_title = '<title>Exchange Tower</title>'
        expected_letting = 'Exchange Tower'

        assert expected_title in content
        assert expected_letting in content
        assert response.status_code == 200
        assertTemplateUsed(response, 'letting.html')

    def test_view_letting_should_return_404(self):
        response = self.client.get(reverse('letting', kwargs={'letting_id': 3}))
        assert response.status_code == 404


class TestLettingUrl(LettingTestCase):
    def test_url_index(self):
        path = reverse('lettings_index')
        assert path == '/lettings/'
        assert resolve(path).view_name == 'lettings_index'

    def test_url_detail(self):
        path = reverse('letting', kwargs={'letting_id': 2})
        assert path == '/lettings/2/'
        assert resolve(path).view_name == 'letting'


class TestLettingModel(LettingTestCase):
    def test_address_model(self):
        address = Address.objects.get(id=1)
        expected_value = '1 Sukhumvit'
        assert str(address) == expected_value

    def test_letting_model(self):
        letting = Letting.objects.get(id=2)
        expected_value = 'Exchange Tower'
        assert str(letting) == expected_value
