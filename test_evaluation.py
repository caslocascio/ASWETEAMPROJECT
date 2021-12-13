import sys
from pathlib import Path
import unittest
from evaluation import app
# import db
sys.path[0] = str(Path(sys.path[0]).parent)


class Test_Testevaluation(unittest.TestCase):

    def setUp(self):
        """Set"""
        # initialize app for testing
        self.app = app.test_client()
        # initialize database
        # self.db = db.init_db()

    def test_main_page(self):
        """Test service landing page"""
        print("entered test_main_page")
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
        print("entered test_professor_endpoint")
        response = self.app.get('/professor?profname=Gail Kaiser')
        review = response.get_json()['reviews']
        # success response
        self.assertEqual(200, response.status_code)
        # check response message
        assert 'Gail Kaiser' in review

    def test_summary_endpoint(self):
        """Test that a summary is returned for a given professor"""
        print("entered test_summary_endpoint")
        response = self.app.get('/summary?profname=Yuanjia Wang')
        summaryProf = response.get_json()['professor_name']
        # success response
        self.assertEqual(200, response.status_code)
        # check response message
        self.assertEqual(summaryProf, 'Yuanjia Wang')

    # get_easy is called within easy_endpoint so coverage should be there
    def test_easy_endpoint_professor(self):
        """Test easy API endpoint for ease information regarding a professor
           like lenient grading, recommend, etc"""
        print("entered test_easy_endpoint_professor")
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

    def test_easy_endpoint_course(self):
        """Test easy API endpoint for ease information regarding a course
           like lenient grading, recommend, etc"""
        print("entered test_easy_endpoint_course")
        response = self.app.get('/easy?course=Metaphysics&profname=')
        # success response
        self.assertEqual(200, response.status_code)
        # check response message
        self.assertEqual(
            response.get_json(),
            {'easy_A': 1,
             'A_plus': 0,
             'lenient_grading': 0,
             'I_recommend': 0}
        )

    # get_final is called within final_endpoint so coverage should be there
    def test_final_endpoint(self):
        """Test final API endpoint for final information regarding a course
           like no final, final paper, etc"""
        print("entered test_final_endpoint")
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
        print("entered test_extensions_endpoint")
        response = self.app.get('/extensions?profname=Eugene Wu')
        # success response
        self.assertEqual(200, response.status_code)
        # check response message
        self.assertEqual(
            response.get_json(),
            {'extension_status': 'no sign prof gives extensions'}
        )

    # get_difficulty is called within difficulty_endpoint so should cover
    def test_difficulty_endpoint_course(self):
        """Test difficulty API endpoint for difficulty information
           regarding a course like hard, boring, etc"""
        print("entered test_difficulty_endpoint_course")
        response = self.app.get(
            '/difficulty?course=Calculus I&profname=')
        # success response
        self.assertEqual(200, response.status_code)
        # check response message
        self.assertEqual(
            response.get_json(),
            {'harsh_grading': 0,
             'boring': 4,
             'hard': 14,
             'not_recommended': 1}
        )

    def test_difficulty_endpoint_professor(self):
        """Test difficulty API endpoint for difficulty information
           regarding a professor like hard, boring, etc"""
        print("entered test_difficulty_endpoint_professor")
        response = self.app.get(
            '/difficulty?profname=Achille Varzi&course=')
        # success response
        self.assertEqual(200, response.status_code)
        # check response message
        self.assertEqual(
            response.get_json(),
            {'harsh_grading': 0,
             'boring': 5,
             'hard': 8,
             'not_recommended': 0}
        )

    def test_review_counts(self):
        """Test the API of review review counts"""
        print("entered test_review_counts")
        response = self.app.get('/total_reviews?profname=Aaron Fox')
        # success response
        self.assertEqual(200, response.status_code)
        # check response message
        self.assertEqual(
            response.get_json(),
            {'professor_name': 'Aaron Fox',
             'total_reviews': 7}
        )

    # test_classes_endpoint calls upon compare and find_class() so should cover
    def test_classes_endpoint_language(self):
        '''Test that classes endpoint returns a list of desired
           type classes like language in order of difficulty, ease or
           if the class includes finals'''
        print("entered test_classes_endpoint_language")
        response = self.app.get(
            '/classes?classtype=language&comparatortype=difficulty')
        # success response
        self.assertEqual(200, response.status_code)
        # check response message
        self.maxDiff = None
        self.assertEqual(
            response.get_json(),
            {'class_results': [['V1101-V1102 Elementary Spanish', 0],
                               ['Intermediate Italian II', 0],
                               [' Elementary Italian I', 1],
                               ['English Lit 1500-1600', 1],
                               ['Elementary French I', 2]]}
        )

    def test_classes_endpoint_math(self):
        '''Test that classes endpoint returns a list of desired
           type classes like math in order of difficulty, ease or
           if the class includes finals'''
        print("entered test_classes_endpoint_math")
        response = self.app.get(
            '/classes?classtype=math&comparatortype=easy')
        # success response
        self.assertEqual(200, response.status_code)
        # check response message
        self.maxDiff = None
        self.assertEqual(
            response.get_json(),
            {'class_results': [['Principles of Applied Mathematics', 0],
                               ['Math Methods: Financial Price Analysis', 0],
                               ['Multivariable Calculus for Engineers' +
                                ' and Applied Scientists', 0],
                               ['Calculus I', 9],
                               ['Calculus III', 33]]}
        )

    def test_classes_endpoint_art(self):
        '''Test that classes endpoint returns a list of desired
           type classes like art in order of difficulty, ease or
           if the class includes finals'''
        print("entered test_classes_endpoint_art")
        response = self.app.get(
            '/classes?classtype=art&comparatortype=difficulty')
        # success response
        self.assertEqual(200, response.status_code)
        # check response message
        self.maxDiff = None
        self.assertEqual(
            response.get_json(),
            {'class_results': [['Late 20th Century Art', 0],
                               ['Arts and Humanities in the City', 0],
                               ['Introduction to the History' +
                                ' of Photography', 1],
                               ['W3650 20th Century Art', 1],
                               ['20th Century Art', 2]]}
        )

    def test_classes_endpoint_computer_science(self):
        '''Test that classes endpoint returns a list of desired
           type classes like math in order of difficulty, ease or
           if the class includes finals'''
        print("entered test_classes_endpoint_computer_science")
        response = self.app.get(
            '/classes?classtype=computer science&comparatortype=final')
        # success response
        self.assertEqual(200, response.status_code)
        # check response message
        self.maxDiff = None
        self.assertEqual(
            response.get_json(),
            {'class_results': [['Computer Science Theory: Computability ' +
                                '- Models - Computation', 0],
                               ['Intro to Computer Science- Programming ' +
                                'in Java', 0],
                               ['Intro to Computer Science- ' +
                                'Programming in C', 0],
                               ['Applied Machine Learning', 0],
                               ['Artificial Intelligence', 0]]}
        )

    def test_review_ages(self):
        '''Test the API of counting old and new reviews'''
        print("entered test_review_ages")
        response = self.app.get('/review_ages/2009-12-31?profname=Aaron Fox')
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
        print("entered test_sentiment_analysis")
        # 1) test this endpoint by professor name
        response = self.app.get('/sentiment?profname=Aaron Fox')
        # success response
        self.assertEqual(200, response.status_code)
        # check partial response because the full response is too long
        partial_response = {k: v for k, v in response.get_json().items()
                            if k != 'details'}
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
        # success response
        self.assertEqual(200, response.status_code)
        # check partial response because the full response is too long
        partial_response = {k: v for k, v in response.get_json().items()
                            if k != 'details'}
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
        print("entered test_recommend_professor")
        response = self.app.get(
            '/recommendProfessor?course=User Interface Design')
        # success response
        self.assertEqual(200, response.status_code)
        # check response message
        self.assertEqual(
            response.get_json(),
            {'professor_name': 'Brian Smith'}
        )


if __name__ == '__main__':
    unittest.main()
