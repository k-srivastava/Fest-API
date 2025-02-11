import unittest
from decimal import Decimal
from typing import Any, Optional

from starlette.testclient import TestClient

import main
from tests import core

PASS_JSON = {
    'name': 'Sports', 'description': 'The definitive sports pass. Access both sports and e-sports events.',
    'cost': Decimal(299).to_eng_string()
}

PASS_ID: Optional[int] = None


class PassTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(main.app)
        core.setup_tests(main.app)

        cls.pass_id = None

    @classmethod
    def tearDownClass(cls):
        core.teardown_tests()

    def assert_pass_is_equal(self, data: dict[str, Any], name: str, description: str, cost: str):
        self.assertEqual(name, data['name'])
        self.assertEqual(description, data['description'])
        self.assertEqual(cost, data['cost'])

    def test_1_create_pass(self):
        response = self.client.post('/pass/', json=PASS_JSON)

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()
        self.assert_pass_is_equal(data, PASS_JSON['name'], PASS_JSON['description'], '299.00')
        self.assertTrue('id' in data)

        global PASS_ID
        PASS_ID = data['id']

    def test_2_read_pass(self):
        response = self.client.get(f'/pass/{PASS_ID}/')

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()
        self.assertEqual(PASS_ID, data['id'])
        self.assert_pass_is_equal(data, PASS_JSON['name'], PASS_JSON['description'], '299.00')

    def test_3_read_all_passes(self):
        self.client.post('/pass/', json=PASS_JSON)

        response = self.client.get('/pass/')
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()
        self.assertEqual(2, len(data))

        self.assert_pass_is_equal(data[0], PASS_JSON['name'], PASS_JSON['description'], '299.00')
        self.assert_pass_is_equal(data[1], PASS_JSON['name'], PASS_JSON['description'], '299.00')

    def test_4_update_pass(self):
        response = self.client.patch(f'/pass/{PASS_ID}/', json={'description': 'New Sports'})

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()
        self.assertEqual(PASS_ID, data['id'])
        self.assert_pass_is_equal(data, PASS_JSON['name'], 'New Sports', '299.00')

    def test_5_delete_pass(self):
        response = self.client.delete(f'/pass/{PASS_ID}/')

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()
        self.assertEqual(PASS_ID, data['id'])

        response = self.client.get(f'/pass/{PASS_ID}/')
        self.assertEqual(404, response.status_code)
        self.assertIsNotNone(response.text)
