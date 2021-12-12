import unittest
import db


class Test_Testdb(unittest.TestCase):
    def setUp(self):
        self.assertTrue(db.init_db())

    def test_get_prof(self):
        # test get_entry_prof from db, using 'Aaron Fox'
        # each entry should have the name of the prof at entry[0]
        ls = db.get_entry_professor('Gail Kaiser')
        # print("this is ls prof")
        # print(ls)
        for entry in ls:
            self.assertEqual(entry[0], 'Gail Kaiser')

    def test_get_class(self):
        # test get_entry_class from db, using 'Introduction to Urban Studies'
        # each entry should have the name of course at entry[1]
        ls = db.get_entry_class('Introduction to Urban Studies')
        # print("this is ls class")
        # print(ls)
        for entry in ls:
            self.assertEqual(entry[1], 'Introduction to Urban Studies')

    def test_get_date(self):
        # test get_entry_date from db, using 'December 31, 1999'
        # each entry should have the date of review at entry[2]
        ls = db.get_entry_date('December 31, 1999')
        # print("this is ls date")
        # print(ls)
        for entry in ls:
            self.assertEqual(entry[2], 'December 31, 1999')

    def test_get_funny(self):
        # test get_entry_funny, using '5' as test
        # each entry should have the students funny score at entry[7]
        ls = db.get_entry_funny(5)
        # print("this is ls funny")
        # print(ls)
        for entry in ls:
            self.assertEqual(entry[7], 5)

    def test_get_agree(self):
        # test get_entry_agree, using '1' as test
        # each entry should have the students agreeability score at entry[5]
        ls = db.get_entry_agree(1)
        # print("this is ls agree")
        # print(ls)
        for entry in ls:
            self.assertEqual(entry[5], 1)

    def test_get_disagree(self):
        # test get_entry_disagree, using '2' as test
        # each entry should have the students agreeability score at entry[6]
        ls = db.get_entry_disagree(2)
        # print("this is ls disagree")
        # print(ls)
        for entry in ls:
            self.assertEqual(entry[6], 2)

    def test_add_entry(self):
        test_entry = ("test", "test", "test", "test", "test", "1", "1", "1")
        self.assertTrue(db.add_entry(test_entry))

    '''
    # this will clear all entries in the db
    # this works already, but don't call it because it takes a long time
    # to reconstruct the table...
    def test_clear_db(self):
        self.assertTrue(db.clear())
    '''
    
if __name__ == '__main__':
    unittest.main()
