import unittest
import scraper


class Test_Scraper(unittest.TestCase):
    def setUp(self):
        self.BaseURL = "https://culpaarchive.herokuapp.com"

    def tearDown(self):
        pass

    def test_getProfs(self):
        # test getProfs method
        profs = scraper.getProfs(self.BaseURL)
        self.assertEqual(len(profs), 1656)

    def test_getProfReview(self):
        # test getProfReview method
        answer = ['"Agnieszka Legutko","Elementary Yiddish II","July 14, 2017",\
"Agi is a lovely person with a fascinating story (she\'s a \
Polish Jewish Yiddishist). She\'s very approachable and \
definitely wants everyone in her class to succeed. \
I took this class in Spring 2017 so, unfortunately, \
I don\'t think I saw her at her best. She experienced \
some personal issues which we were all very sympathetic \
and flexible about but at a certain point it became \
clear that she should\'ve taken time off instead of \
continuing to work. She became forgetful and distracted \
(again, totally fair and human, just not conducive to \
teaching) to the point where she thought our Final \
started an hour later than it had been scheduled. \
As a person I understood but as a student her lack \
of organization/energy really frustrated and stressed \
me out as a student. The other thing I would say is \
that she is a better teacher for higher levels. \
There were several moments where some of the more \
adept students just answered other students\' \
questions for her because she didn\'t understand \
their question or explain the concept well. Again, \
I don\'t think Agi is a bad teacher, but I do think \
there are some things (whether temporary or permanent) \
that she could work on. ","There are homeworks from the \
book and packet, quizzes, a few journal entries, and a \
final. Overall pretty straightforward but it\'s important \
to stay on top of because it can be hard to catch up. \
You\'re pretty much expected to come to class to, \
y\'know, speak the language. The one other note I would \
say is that the Yiddish department takes off for Jewish \
holidays! (Whether you\'re Jewish or not this is a good \
thing to know).",1,0,0\n']
        profs = scraper.getProfs(self.BaseURL)
        self.assertEqual([e for e in scraper.getProfReview(self.BaseURL +
                          profs[20]['href'], profs[20].text)], answer)
