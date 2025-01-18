import unittest
from fastapi.testclient import TestClient
from analytics_server import app, init_db
import sqlite3

class TestEventProcessing(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Initialize the database before running tests
        init_db()

    def setUp(self):
        # Clear the database before each test
        connection = sqlite3.connect('analytics.db')
        cursor = connection.cursor()
        cursor.execute('DELETE FROM events')
        connection.commit()
        connection.close()
        self.client = TestClient(app)

    def test_insert_valid_event(self):
        payload = {
            "userid": "user123",
            "eventname": "login"
        }
        response = self.client.post("/process_event", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Event processed successfully.")

        # Verify the event is in the database
        connection = sqlite3.connect('analytics.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM events WHERE userid = ? AND eventname = ?', ("user123", "login"))
        rows = cursor.fetchall()
        self.assertEqual(len(rows), 1)
        connection.close()

    def test_missing_userid(self):
        payload = {
            "eventname": "login"
        }
        response = self.client.post("/process_event", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Both userid and eventname are required.")

    def test_missing_eventname(self):
        payload = {
            "userid": "user123"
        }
        response = self.client.post("/process_event", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Both userid and eventname are required.")

    def test_empty_payload(self):
        response = self.client.post("/process_event", json={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Both userid and eventname are required.")

if __name__ == "__main__":
    unittest.main()
