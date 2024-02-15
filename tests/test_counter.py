# test_couter.py


"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""
import json
from unittest import TestCase
from src.counter import app
# Ensure status codes are imported correctly
from src import status

class CounterTest(TestCase):
    def setUp(self):
        self.client = app.test_client()


    def test_duplicate_a_counter(self):
        """It should return an error for duplicates"""
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)

    def test_increment(self):
        result = self.client.put('/counters/goo')
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)

        result = self.client.post('/counters/goo')

        result = self.client.put('/counters/goo')
        self.assertEqual(result.status_code, status.HTTP_200_OK)


    def test_get_value(self):
        result = self.client.get('/counters/foo')
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)

        result = self.client.post('/counters/foo')

        result = self.client.put('/counters/foo')

        result = self.client.get('/counters/foo')

        response_data = result.get_json()

        self.assertEqual(response_data['foo'], 2)

    def test_delete_counter(self):
        """Test deleting an existing counter."""
        self.client.post('/counters/test')  # Create a counter to delete
        delete_result = self.client.delete('/counters/test')
        self.assertEqual(delete_result.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify the counter is deleted
        get_result = self.client.get('/counters/test')
        self.assertEqual(get_result.status_code, status.HTTP_404_NOT_FOUND)


