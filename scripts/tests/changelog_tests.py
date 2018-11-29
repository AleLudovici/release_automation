from scripts.changelog import *
from requests import Response


def test_given_a_token_then_it_builds_the_issues_url_correctly(monkeypatch):
    def mocked_get(uri, *args, **kwargs):
        assert uri == "https://api.github.com/repos/AleLudovici/release_automation/issues"
        assert kwargs == {'params': {'Authorization: token': '0123456789ABCDEF', 'state': 'closed'}}
        mock_response = Response()
        mock_response.status_code = 201
        return mock_response

    monkeypatch.setattr(requests, 'get', mocked_get)
    build_issues_requests('test_credentials.txt')
