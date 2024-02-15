from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIClient


class GithubProxyTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    @patch('api.views.github_proxy.requests')
    @patch('api.views.github_proxy.GITHUB_TOKEN', 'TOKEN')
    def test_github_proxy(self, mock_requests):
        mock_requests.get.return_value.status_code = 200
        mock_requests.get.return_value.json = lambda: {'test': 'data'}

        response = self.client.get('/api/github/proxy?url=https://api.github.com/test/url')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'test': 'data'})
        mock_requests.get.assert_called_with('https://api.github.com/test/url',
                                             headers={'Authorization': 'Bearer TOKEN'})

    @patch('api.views.github_proxy.GITHUB_TOKEN', 'TOKEN')
    # @patch('api.views.github_proxy.GithubRequestException')
    @patch('api.views.github_proxy.requests')
    def test_github_proxy_github_error(self, mock_requests):
        mock_requests.get.return_value.status_code = 400
        # mock_exception.return_value = Exception()

        response = self.client.get('/api/github/proxy?url=https://api.github.com/incorrect/url')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, None)
        # mock_exception.assert_called()

    @patch('api.views.github_proxy.GITHUB_TOKEN', 'TOKEN')
    # @patch('api.views.github_proxy.GithubRequestException')
    def test_github_proxy_missing_url(self):
        # mock_exception.return_value = Exception()

        response = self.client.get('/api/github/proxy')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, None)
        # mock_exception.assert_called()
