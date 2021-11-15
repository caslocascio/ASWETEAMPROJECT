import sys
from pathlib import Path
import unittest
from evaluation import app
import db
sys.path[0] = str(Path(sys.path[0]).parent)


class Test_Testevaluation(unittest.TestCase):

    def setUp(self):
        """Set"""
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

    def test_easy_endpoint(self):
        """Test easy API endpoint for ease information regarding a professor
           like lenient grading, recommend, etc"""
        response = self.app.get('/easy?profname=Aaron Fox')
        print(response.get_json())
        # success response
        self.assertEqual(200, response.status_code)
        # check response message
        self.assertEqual(
            response.get_json(),
            {'easy_A': 0,
             'A_plus': 0,
             'lenient_grading': 0,
             'I_recommend': 1}
        )

    def test_final_endpoint(self):
        """Test final API endpoint for final information regarding a course
           like no final, final paper, etc"""
        response = self.app.get('/final?course=Introduction to Urban Studies')
        print(response.get_json())
        # success response
        self.assertEqual(200, response.status_code)
        # check response message
        self.assertEqual(
            response.get_json(),
            {'final_exam': 'no indicator that class is final exam free'}
        )

    def test_extensions_endpoint(self):
        """Test extensions API endpoint for extension
           information regarding a professor"""
        response = self.app.get('/extensions?profname=Aaron Fox')
        print(response.get_json())
        # success response
        self.assertEqual(200, response.status_code)
        # check response message
        self.assertEqual(
            response.get_json(),
            {'extension_status': 'no indicator prof gives extensions'}
        )

    def test_difficulty_endpoint(self):
        """Test difficulty API endpoint for difficulty information
           regarding a course like hard, boring, etc"""
        response = self.app.get('/difficulty?\
                                course=Introduction to Urban Studies')
        print(response.get_json())
        # success response
        self.assertEqual(200, response.status_code)
        # check response message
        self.assertEqual(
            response.get_json(),
            {'difficulty_status': 'no indicator course is too tough'}
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

    """
    Commenting these two endpoints out as they need a bit more work
    which will be completed by the second iteration.
    """

    """

    def test_review_ages(self):
        '''Test the API of counting old and new reviews'''
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
        '''Test the API of sentiment analysis'''
        response = self.app.get('/sentiment?profname=Aaron Fox')
        print(response.get_json())
        # success response
        self.assertEqual(200, response.status_code)
        # check partial response because the full response is too long
        partial_response = {k: v for k, v in response.get_json().items()
                            if k != 'details'}
        print(partial_response)
        self.assertEqual(
            partial_response,
            {'professor_name': 'Aaron Fox',
             'positive_reviews': '3',
             'neutral_reviews': '2',
             'negative_reviews': '1',
             'objective_reviews': '4',
             'subjective_reviews': '2'}
        )

    """


if __name__ == '__main__':
    unittest.main()
