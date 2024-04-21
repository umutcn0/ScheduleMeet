from django.test import TestCase, Client
from datetime import datetime
import json

class MeetHandlerTestCase(TestCase):
    def setUp(self):
        # Her test başlamadan önce kullanıcıları ve bir client oluşturuyoruz.
        self.client = Client()

    def test_create_meet(self):
        # Yeni bir toplantı oluşturup, JSON yanıtını kontrol ediyoruz.
        response = self.client.post(
            '/meet/handler/',
            data='{"date": "2024-02-15", "start_hour": "10:00:00", "end_hour": "12:00:00", "description": "Test Meeting", "participants": "john@example.com"}',
            content_type='application/json'
        )
        response_json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['success'], True)
        self.assertEqual(response_json['message'], 'Meeting created successfully')

    def test_update_meet(self):
        # Yeni bir toplantı oluşturuyoruz.
        response_create = self.client.post(
            '/meet/handler/',
            data='{"date": "2024-02-15", "start_hour": "10:00:00", "end_hour": "12:00:00", "description": "Test Meeting", "participants": "john@example.com"}',
            content_type='application/json'
        )
        self.assertEqual(response_create.status_code, 200)
        meet_id = response_create.json().get('id')

        # Oluşturulan toplantıyı güncelliyoruz.
        response_update = self.client.put(
            '/meet/handler/',
            data='{"id": ' + str(meet_id) + ', "date": "2024-02-16", "start_hour": "11:00:00", "end_hour": "13:00:00", "description": "Updated Meeting", "participants": "jane@example.com"}',
            content_type='application/json'
        )
        response_update_json = response_update.json()

        self.assertEqual(response_update.status_code, 200)
        self.assertEqual(response_update_json['success'], True)
        self.assertEqual(response_update_json['message'], 'Meeting updated successfully')

    def test_delete_meet(self):
        # Yeni bir toplantı oluşturuyoruz.
        data = {
            'date': '2024-02-15',
            'start_hour': '10:00:00',
            'end_hour': '12:00:00',
            'description': 'Test Meeting',
            'participants': 'john@example.com'
        }
        response_create = self.client.post(
            '/meet/handler/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response_create.status_code, 200)
        meet_id = response_create.json().get('id')

        # Oluşturulan toplantıyı siliyoruz.
        response_delete = self.client.delete(
            '/meet/handler/',
            data=json.dumps({"id": meet_id}),
            content_type='application/json'
        )
        response_delete_json = response_delete.json()
        print(response_delete_json)

        self.assertEqual(response_delete.status_code, 200)
        self.assertEqual(response_delete_json['success'], True)
        self.assertEqual(response_delete_json['message'], 'Meeting deleted successfully')

if __name__ == '__main__':
    import unittest
    unittest.main()
