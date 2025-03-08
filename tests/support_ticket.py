import unittest
from datetime import datetime
from typing import Any, Optional

from starlette import status
from starlette.testclient import TestClient

import main
from db.core import SupportTicketCategory
from tests import core

SUPPORT_TICKET_JSON = {
    'name': 'API Is Broken', 'description': 'The API is fried to a crisp.',
    'category': SupportTicketCategory.SPECIAL_REQUEST.value, 'timestamp': datetime(2025, 1, 1, 12, 0, 0).isoformat(),
    'solved': False, 'college_name': 'MIT-B', 'email_address': None, 'phone_number': None, 'solved_email_address': None,
    'comment': None
}

SUPPORT_TICKET_ID: Optional[str] = None


class SupportTicketTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(main.app)
        cls.headers = core.get_default_headers()

        core.setup_tests(main.app)

    @classmethod
    def tearDownClass(cls):
        core.teardown_tests()

    def assert_support_ticket_is_equal(
            self, data: dict[str, Any], name: str, description: str, category: SupportTicketCategory,
            timestamp: str, solved: bool, college_name: Optional[str], email_address: Optional[str],
            phone_number: Optional[str], solved_email_address: Optional[str], comment: Optional[str]
    ):
        self.assertEqual(name, data['name'])
        self.assertEqual(description, data['description'])
        self.assertEqual(category, data['category'])
        self.assertEqual(timestamp, data['timestamp'])
        self.assertEqual(solved, data['solved'])
        self.assertEqual(college_name, data['college_name'])
        self.assertEqual(email_address, data['email_address'])
        self.assertEqual(phone_number, data['phone_number'])
        self.assertEqual(solved_email_address, data['solved_email_address'])
        self.assertEqual(comment, data['comment'])

    def test_1_create_support_ticket(self):
        response = self.client.post('/support-ticket/', json=SUPPORT_TICKET_JSON, headers=self.headers)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()

        self.assert_support_ticket_is_equal(
            data, SUPPORT_TICKET_JSON['name'], SUPPORT_TICKET_JSON['description'], SUPPORT_TICKET_JSON['category'],
            SUPPORT_TICKET_JSON['timestamp'], SUPPORT_TICKET_JSON['solved'], SUPPORT_TICKET_JSON['college_name'],
            SUPPORT_TICKET_JSON['email_address'], SUPPORT_TICKET_JSON['phone_number'],
            SUPPORT_TICKET_JSON['solved_email_address'], SUPPORT_TICKET_JSON['comment']
        )
        self.assertTrue('id' in data)

        global SUPPORT_TICKET_ID
        SUPPORT_TICKET_ID = data['id']

    def test_2_read_support_ticket(self):
        response = self.client.get(f'/support-ticket/{SUPPORT_TICKET_ID}/', headers=self.headers)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()

        self.assertEqual(SUPPORT_TICKET_ID, data['id'])
        self.assert_support_ticket_is_equal(
            data, SUPPORT_TICKET_JSON['name'], SUPPORT_TICKET_JSON['description'], SUPPORT_TICKET_JSON['category'],
            SUPPORT_TICKET_JSON['timestamp'], SUPPORT_TICKET_JSON['solved'], SUPPORT_TICKET_JSON['college_name'],
            SUPPORT_TICKET_JSON['email_address'], SUPPORT_TICKET_JSON['phone_number'],
            SUPPORT_TICKET_JSON['solved_email_address'], SUPPORT_TICKET_JSON['comment']
        )

    def test_3_mark_unsolved_support_ticket(self):
        response = self.client.post(f'/support-ticket/{SUPPORT_TICKET_ID}/?solved=False', headers=self.headers)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()
        self.assertEqual(SUPPORT_TICKET_ID, data['id'])

    def test_4_mark_solved_support_ticket(self):
        response = self.client.post(
            f'/support-ticket/{SUPPORT_TICKET_ID}/?solved=True&email_address=abc@def.com', headers=self.headers
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()
        self.assertEqual(SUPPORT_TICKET_ID, data['id'])
        self.assert_support_ticket_is_equal(
            data, SUPPORT_TICKET_JSON['name'], SUPPORT_TICKET_JSON['description'], SUPPORT_TICKET_JSON['category'],
            SUPPORT_TICKET_JSON['timestamp'], True, SUPPORT_TICKET_JSON['college_name'],
            SUPPORT_TICKET_JSON['email_address'], SUPPORT_TICKET_JSON['phone_number'], 'abc@def.com',
            SUPPORT_TICKET_JSON['comment']
        )

    def test_5_update_support_ticket(self):
        response = self.client.patch(
            f'/support-ticket/{SUPPORT_TICKET_ID}/',
            json={'phone_number': '9876543210', 'comment': 'Working on a fix.'}, headers=self.headers
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()
        self.assertEqual(SUPPORT_TICKET_ID, data['id'])
        self.assert_support_ticket_is_equal(
            data, SUPPORT_TICKET_JSON['name'], SUPPORT_TICKET_JSON['description'], SUPPORT_TICKET_JSON['category'],
            SUPPORT_TICKET_JSON['timestamp'], True, SUPPORT_TICKET_JSON['college_name'],
            SUPPORT_TICKET_JSON['email_address'], '9876543210', 'abc@def.com',
            'Working on a fix.'
        )

    def test_6_delete_support_ticket(self):
        response = self.client.delete(f'/support-ticket/{SUPPORT_TICKET_ID}/', headers=self.headers)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()
        self.assertEqual(SUPPORT_TICKET_ID, data['id'])

        response = self.client.get(f'/support-ticket/{SUPPORT_TICKET_ID}/', headers=self.headers)

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertIsNotNone(response.text)
