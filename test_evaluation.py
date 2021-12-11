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
        # success response
        self.assertEqual(200, response.status_code)
        # check response message
        self.assertEqual(
            response.get_json(),
            {'msg': 'ItWorksOnLocal Service'}
        )

    def test_professor_endpoint(self):
        """Test that the singular review being returned is for correct prof"""
        response = self.app.get('/professor?profname=Gail Kaiser')
        review = response.get_json()['reviews']
        # success response
        self.assertEqual(200, response.status_code)
        # check response message
        assert 'Gail Kaiser' in review

    def test_summary_endpoint(self):
        """Test that a summary is returned for a given professor"""
        response = self.app.get('/summary?profname=Yuanjia Wang')
        summaryProf = response.get_json()['professor_name']
        # success response
        self.assertEqual(200, response.status_code)
        # check response message
        self.assertEqual(summaryProf, 'Yuanjia Wang')

    # get_easy is called within easy_endpoint so coverage should be there
    def test_easy_endpoint(self):
        """Test easy API endpoint for ease information regarding a professor
           like lenient grading, recommend, etc"""
        response = self.app.get('/easy?profname=Aaron Fox&course=')
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

    # get_final is called within final_endpoint so coverage should be there
    def test_final_endpoint(self):
        """Test final API endpoint for final information regarding a course
           like no final, final paper, etc"""
        response = self.app.get('/final?course=Introduction to Urban Studies')
        # success response
        self.assertEqual(200, response.status_code)
        # check response message
        self.assertEqual(
            response.get_json(),
            {'final_exam': 'no sign class is final exam free'}
        )

    def test_extensions_endpoint(self):
        """Test extensions API endpoint for extension
           information regarding a professor"""
        response = self.app.get('/extensions?profname=Eugene Wu')
        # success response
        self.assertEqual(200, response.status_code)
        # check response message
        self.assertEqual(
            response.get_json(),
            {'extension_status': 'no sign prof gives extensions'}
        )

    # get_difficulty is called within difficulty_endpoint so should cover
    def test_difficulty_endpoint(self):
        """Test difficulty API endpoint for difficulty information
           regarding a course like hard, boring, etc"""
        response = self.app.get(
            '/difficulty?course=Machine Learning&profname=')
        # success response
        self.assertEqual(200, response.status_code)
        # check response message
        self.assertEqual(
            response.get_json(),
            {'boring': 2,
             'hard': 4,
             'harsh_grading': 0,
             'not_recommended': 0}
        )

    def test_review_counts(self):
        """Test the API of review review counts"""
        response = self.app.get('/total_reviews?profname=Aaron Fox')
        # success response
        self.assertEqual(200, response.status_code)
        # check response message
        self.assertEqual(
            response.get_json(),
            {'professor_name': 'Aaron Fox',
             'total_reviews': 7}
        )

    # WINSTON NEEDS TO FIX THIS
    # test_classes_endpoint calls upon compare and find_class() so should cover
    def test_classes_endpoint(self):
        """Test that classes endpoint returns a list of desired
           type classes like math in order of difficulty, ease or
           if the class includes finals """
        response = self.app.get(
            '/classes?classtype=language&comparatortype=difficulty')
        print("this is response in test classes")
        print(response)
        print("this is response.json() in test classes")
        print(response.get_json())
        # success response
        self.assertEqual(200, response.status_code)
        # check response message
        self.assertEqual(
            response.get_json(),
            {'hello': 'hi'}
        )

    # Danni's testing

    def test_review_ages(self):
        '''Test the API of counting old and new reviews'''
        response = self.app.get('/review_ages/2009-12-31?profname=Aaron Fox')
        print(response.get_json())
        # success response
        self.assertEqual(200, response.status_code)
        # check response message
        self.assertEqual(
            response.get_json(),
            {'professor_name': 'Aaron Fox',
             'threshold': '2009-12-31',
             'new_reviews': 1,
             'old_reviews': 6}
        )

    def test_sentiment_analysis(self):
        '''Test the API of sentiment analysis'''
        # 1) test this endpoint by professor name
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
             'positive_reviews': '4',
             'neutral_reviews': '2',
             'negative_reviews': '1',
             'objective_reviews': '4',
             'subjective_reviews': '3'}
        )
        # 2) test this endpoint by class name
        response = self.app.get(
            '/sentiment?course=Methods and Problems of Philosophical Thought')
        print(response.get_json())
        # success response
        self.assertEqual(200, response.status_code)
        # check partial response because the full response is too long
        partial_response = {k: v for k, v in response.get_json().items()
                            if k != 'details'}
        print(partial_response)
        self.assertEqual(
            partial_response,
            {'professor_name': None,
             'positive_reviews': '14',
             'neutral_reviews': '15',
             'negative_reviews': '2',
             'objective_reviews': '15',
             'subjective_reviews': '16'}
        )

    def test_recommend_professor(self):
        """Test the API of recommend professor"""
        response = self.app.get('/recommendProfessor?course=User Interface Design')
        # success response
        self.assertEqual(200, response.status_code)
        # check response message
        self.assertEqual(
            response.get_json(),
            {'professor_name': 'Lydia Chilton'}
        )


if __name__ == '__main__':
    unittest.main()
