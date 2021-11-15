
import sys
from pathlib import Path
sys.path[0] = str(Path(sys.path[0]).parent)
import unittest
import json
from main import app
from functions import db

class TestApi(unittest.TestCase):

    def setUp(self):
        """ Set"""
        # initialize app for testing
        self.app = app.test_client()
        # initialize database
        self.db = db.init_db()

    def test_main_page(self):
        """Test service landing page"""
        response = self.app.get("/")
        print(response.get_json())
        # success response
        self.assertEqual(200, response.status_code)
        # check response message 
        self.assertEqual(
            response.get_json(),
            {'msg': 'ItWorksOnLocal Service'},
        )

    def test_review_counts(self):
        """Test the API of review review counts"""
        response = self.app.get('/total_reviews?profname=Aaron Fox')
        print(response.get_json())
        # success response
        self.assertEqual(200, response.status_code)
        # check response message 
        self.assertEqual(
            response.get_json(),
            {'professor_name': 'Aaron Fox',
             'total_reviews': 6}
        )

    def test_review_ages(self):
        """Test the API of counting old and new reviews"""
        response = self.app.post('/review_ages/2009-12-31?profname=Aaron Fox')
        print(response.get_json())
        # success response
        self.assertEqual(200, response.status_code)
        # check response message 
        self.assertEqual(
            response.get_json(),
            {'professor_name': 'Aaron Fox',
             'threshold': '2009-12-31',
             'new_reviews': 1,
             'old_reviews': 5}
        )

    def test_sentiment_analysis(self):
        """Test the API of sentiment analysis"""
        response = self.app.get('/sentiment?profname=Aaron Fox')
        print(response.get_json())
        # success response
        self.assertEqual(200, response.status_code)
        # check partial response because the full response is too long
        partial_response = {k: v for k, v in response.get_json().items() if k != 'details'}
        print(partial_response)
        self.assertEqual(
            partial_response,
            {'professor_name': 'Aaron Fox',
             'postive reviews': '3',
             'neutral reviews': '2',
             'negative reviews': '1',
             'objective reviews': '4',
             'subjective reviews': '2'}
        )

if __name__ == '__main__':
    unittest.main()