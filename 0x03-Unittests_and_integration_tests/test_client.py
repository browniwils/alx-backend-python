#!/usr/bin/env python3
"""A module for testing the client module.
"""

import unittest
from typing import Dict
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from parameterized import parameterized
from parameterized import parameterized_class
from requests import HTTPError
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch
from unittest.mock import PropertyMock


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient class."""

    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"}),
    ])
    @patch("client.get_json")
    def test_org(self, org: str, resp: Dict, mocked_fxn: MagicMock) -> None:
        """Tests for org method."""

        mocked_fxn.return_value = MagicMock(return_value=resp)
        git_client = GithubOrgClient(org)
        self.assertEqual(git_client.org(), resp)
        mocked_fxn.assert_called_once_with(
            f"https://api.github.com/orgs/{org}"
        )

    def test_public_repos_url(self) -> None:
        """Tests for _public_repos_url property."""

        with patch("client.GithubOrgClient.org",
                   new_callable=PropertyMock) as org_mock:
            org_mock.return_value = {
                "repos_url": "https://api.github.com/users/google/repos",
            }
            self.assertEqual(GithubOrgClient("google")._public_repos_url,
                             "https://api.github.com/users/google/repos")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json: MagicMock) -> None:
        """Tests for public_repos method."""
        _payload = {
            "repos_url": "https://api.github.com/users/google/repos",
            "repos": [
                {
                    "id": 7697149,
                    "name": "episodes.dart",
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 1342004,
                    },
                    "fork": False,
                    "url": "https://api.github.com/repos/google/episodes.dart",
                    "created_at": "2013-01-19T00:31:37Z",
                    "updated_at": "2019-09-23T11:53:58Z",
                    "has_issues": True,
                    "forks": 22,
                    "default_branch": "master",
                },
                {
                    "id": 8566972,
                    "name": "kratu",
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 1342004,
                    },
                    "fork": False,
                    "url": "https://api.github.com/repos/google/kratu",
                    "created_at": "2013-03-04T22:52:33Z",
                    "updated_at": "2019-11-15T22:22:16Z",
                    "has_issues": True,
                    "forks": 32,
                    "default_branch": "master",
                },
            ]
        }
        mock_get_json.return_value = _payload["repos"]
        with patch("client.GithubOrgClient._public_repos_url",
                   new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = _payload["repos_url"]
            self.assertEqual(GithubOrgClient("google").public_repos(),
                             ["episodes.dart", "kratu"])
            mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "bsd-3-clause"}}, "bsd-3-clause", True),
        ({"license": {"key": "bsl-1.0"}}, "bsd-3-clause", False),
    ])
    def test_has_license(self, repo: Dict, key: str, expected: bool) -> None:
        """Tests for has_license method."""

        git_client = GithubOrgClient("google")
        client_has_licence = git_client.has_license(repo, key)
        self.assertEqual(client_has_licence, expected)


@parameterized_class([
    {
        "org_payload": TEST_PAYLOAD[0][0],
        "repos_payload": TEST_PAYLOAD[0][1],
        "expected_repos": TEST_PAYLOAD[0][2],
        "apache2_repos": TEST_PAYLOAD[0][3]},
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Testing class performing integration tests for GithubOrgClient class."""

    @classmethod
    def setUpClass(cls) -> None:
        """Setsup fixtures before running tests."""
        route_payload = {
            "https://api.github.com/orgs/google": cls.org_payload,
            "https://api.github.com/orgs/google/repos": cls.repos_payload,
        }

        def get_payload(url):
            if url in route_payload:
                return Mock(**{"json.return_value": route_payload[url]})
            return HTTPError

        cls.get_patcher = patch("requests.get", side_effect=get_payload)
        cls.get_patcher.start()

    def test_public_repos(self) -> None:
        """Tests for public_repos method."""

        self.assertEqual(GithubOrgClient("google").public_repos(),
                         self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """Tests for public_repos method with a license."""

        self.assertEqual(
            GithubOrgClient("google").public_repos(license="apache-2.0"),
            self.apache2_repos)

    @classmethod
    def tearDownClass(cls) -> None:
        """Removes the the setup fixtures after running all tests."""

        cls.get_patcher.stop()
