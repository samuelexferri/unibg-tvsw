from django.test import TestCase
from django.urls import reverse

"""
Views tests
"""


class ViewTest(TestCase):

    def test_homepage(self):
        url = reverse('home')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_signup(self):
        url = reverse('authentication:register')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    # TODO Activate
    """
    def test_activate(self):
        url = reverse('authentication:activate')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
    """

    def test_signin(self):
        url = reverse('authentication:login')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_signout(self):
        url = reverse('authentication:logout')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
