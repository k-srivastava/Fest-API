import unittest

from starlette.testclient import TestClient

import main
from tests import core


class AssociationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(main.app)
        cls.ids = core.get_default_db_ids()
        cls.headers = core.get_default_headers()

        core.setup_tests(main.app)
        core.create_default_test_db()

    @classmethod
    def tearDownClass(cls):
        core.teardown_tests()

    def test_pass_events(self):
        response = self.client.get(f'/pass/{self.ids["all-sports-pass"]}/events/', headers=self.headers)
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()
        self.assertEqual(2, len(data))

    def test_event_passes(self):
        response = self.client.get(f'/event/{self.ids["track&field-event"]}/passes/', headers=self.headers)
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()
        self.assertEqual(3, len(data))

    def test_team_events(self):
        response = self.client.get(f'/team/{self.ids["sports-champs-team"]}/events/', headers=self.headers)
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()
        self.assertEqual(1, len(data))
        self.assertEqual(self.ids["track&field-event"], data[0]['id'])

    def test_event_teams(self):
        response = self.client.get(f'/event/{self.ids["track&field-event"]}/teams/', headers=self.headers)
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()
        self.assertEqual(1, len(data))
        self.assertEqual(self.ids["sports-champs-team"], data[0]['id'])

    def test_team_users(self):
        response = self.client.get(f'/team/{self.ids["sports-champs-team"]}/users/', headers=self.headers)
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()
        self.assertEqual(2, len(data))

    def test_user_teams_host(self):
        response = self.client.get(f'/user/{self.ids["john-smith-user"]}/teams/?host=true', headers=self.headers)
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()
        self.assertEqual(2, len(data))

    def test_user_teams_member(self):
        response = self.client.get(f'/user/{self.ids["john-smith-user"]}/teams/?host=false', headers=self.headers)
        self.assertEqual(200, response.status_code)

        data = response.json()
        self.assertEqual(2, len(data))

    def test_user_events_organizer(self):
        response = self.client.get(f'/user/{self.ids["john-smith-user"]}/events', headers=self.headers)
        self.assertEqual(200, response.status_code)

        data = response.json()
        self.assertEqual(2, len(data))
