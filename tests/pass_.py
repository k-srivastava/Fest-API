import unittest
from decimal import Decimal
from typing import Any

from starlette.testclient import TestClient

import main
from tests import core

PASS_JSON = {
    'name': 'Sports', 'description': 'The definitive sports pass. Access both sports and e-sports events.',
    'cost': Decimal(299).to_eng_string()
}


class PassTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(main.app)
        core.setup_tests(main.app)

    @classmethod
    def tearDownClass(cls):
        core.teardown_tests()

    def assert_pass_is_valid(self, data: dict[str, Any], name: str, description: str, cost: str):
        self.assertEqual(name, data['name'])
        self.assertEqual(description, data['description'])
        self.assertEqual(cost, data['cost'])

    def test_1_create_pass(self):
        response = self.client.post('/pass/', json=PASS_JSON)

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()
        self.assert_pass_is_valid(data, PASS_JSON['name'], PASS_JSON['description'], '299.00')
        self.assertTrue('id' in data)

    def test_2_read_pass(self):
        pass_id = 1
        response = self.client.get(f'/pass/{pass_id}/')

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()
        self.assertEqual(pass_id, data['id'])
        self.assert_pass_is_valid(data, PASS_JSON['name'], PASS_JSON['description'], '299.00')

    def test_3_read_all_passes(self):
        self.client.post('/pass/', json=PASS_JSON)

        response = self.client.get('/pass/')
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()
        self.assertEqual(2, len(data))

        self.assert_pass_is_valid(data[0], PASS_JSON['name'], PASS_JSON['description'], '299.00')
        self.assert_pass_is_valid(data[1], PASS_JSON['name'], PASS_JSON['description'], '299.00')

    def test_4_update_pass(self):
        pass_id = 1
        response = self.client.patch(f'/pass/{pass_id}/', json={'description': 'New Sports'})

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()
        self.assertEqual(pass_id, data['id'])
        self.assert_pass_is_valid(data, PASS_JSON['name'], 'New Sports', '299.00')

    def test_5_delete_pass(self):
        pass_id = 1
        response = self.client.delete(f'/pass/{pass_id}/')

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.text)

        data = response.json()
        self.assertEqual(pass_id, data['id'])

        response = self.client.get(f'/pass/{pass_id}/')
        self.assertEqual(404, response.status_code)
        self.assertIsNotNone(response.text)
