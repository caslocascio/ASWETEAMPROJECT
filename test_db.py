import unittest
import db


class Test_Testdb(unittest.TestCase):
    def setUp(self):
        db.init_db()
        return

    #def tearDown(self):
    #    db.clear()
    #    return

    def test_get_prof(self):
        # test get_entry_prof from db, using 'Aaron Fox'
        # each entry should have the name of the prof at entry[0]
        ls = db.get_entry_professor('Aaron Fox')
        for entry in ls:
            self.assertEqual(entry[0], 'Aaron Fox')

    def test_get_class(self):
        # test get_entry_class from db, using 'Introduction to Urban Studies'
        # each entry should have the name of course at entry[1]
        ls = db.get_entry_class('Introduction to Urban Studies')
        for entry in ls:
            self.assertEqual(entry[1], 'Introduction to Urban Studies')

    def test_get_date(self):
        # test get_entry_date from db, using 'December 31, 1999'
        # each entry should have the date of review at entry[2]
        ls = db.get_entry_date('December 31, 1999')
        for entry in ls:
            self.assertEqual(entry[2], 'December 31, 1999')

    def test_get_funny(self):
        # test get_entry_funny, using '5' as test
        # each entry should have the students funny score at entry[7]
        ls = db.get_entry_funny(5)
        for entry in ls:
            self.assertEqual(entry[7], 5)

    def test_get_agree(self):
        # test get_entry_agree, using '1' as test
        # each entry should have the students agreeability score at entry[5]
        ls = db.get_entry_agree(1)
        for entry in ls:
            self.assertEqual(entry[5], 1)

    def test_get_disagree(self):
        # test get_entry_disagree, using '2' as test
        # each entry should have the students agreeability score at entry[6]
        ls = db.get_entry_disagree(2)
        for entry in ls:
            self.assertEqual(entry[6], 2)


if __name__ == '__main__':
    unittest.main()
