from django.test import Client, TestCase
from django.urls import reverse, resolve
from pytest_django.asserts import assertTemplateUsed

from django.contrib.auth.models import User
from profiles.models import Profile


class ProfileTestCase(TestCase):
    """
    Test class for profile app.
    """
    def setUp(self):
        User.objects.create(
            username='The King',
            email='theking@gmail.com'
        )
        User.objects.create(
            username='The Queen',
            email='thekqueen@gmail.com'
        )

        Profile.objects.create(
            user=User.objects.get(id=1),
            favorite_city='Phuket'
        )
        Profile.objects.create(
            user=User.objects.get(id=2),
            favorite_city='Chiang Mai'
        )
        self.client = Client()


class TestProfileView(ProfileTestCase):
    def test_view_index(self):
        response = self.client.get(reverse('profiles_index'))
        content = response.content.decode()
        expected_title = '<title>Profiles</title>'
        expected_profile = 'The King'

        assert expected_title in content
        assert expected_profile in content
        assert response.status_code == 200
        assertTemplateUsed(response, 'profiles_index.html')

    def test_view_should_return_profile(self):
        response = self.client.get(reverse('profile', kwargs={'username': 'The King'}))
        content = response.content.decode()
        expected_title = '<title>The King</title>'
        expected_favorite_city = '<p>Favorite city: Phuket</p>'

        assert expected_title in content
        assert expected_favorite_city in content
        assert response.status_code == 200
        assertTemplateUsed(response, 'profile.html')

    def test_view_should_return_404(self):
        response = self.client.get(reverse('profile', kwargs={'username': 'The Prince'}))
        assert response.status_code == 404


class TestProfileUrl(ProfileTestCase):
    def test_url_index(self):
        path = reverse('profiles_index')
        assert path == '/profiles/'
        assert resolve(path).view_name == 'profiles_index'

    def test_url_detail(self):
        path = reverse('profile', kwargs={'username': 'The Queen'})
        assert path == '/profiles/The%20Queen/'
        assert resolve(path).view_name == 'profile'


class TestProfileModel(ProfileTestCase):
    def test_user_model(self):
        user = User.objects.get(id=2)
        expected_value = 'The Queen'
        assert str(user) == expected_value

    def test_profile_model(self):
        profile = Profile.objects.get(id=1)
        expected_value = 'The King'
        assert str(profile) == expected_value
