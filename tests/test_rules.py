import unittest
from utils.rules import KeywordRule, ForkRule


class TestKeywordRule(unittest.TestCase):
    def setUp(self):
        self.keyword_rule = KeywordRule(name='Test Keyword', keywords={'test', 'keyword'})
        self.text = 'This is a test text with a keyword.'
        self.checklist = []
        self.result = True

    def test_apply(self):
        expected_result = True
        expected_checklist = [('Test Keyword', 'OK')]
        result, checklist = self.keyword_rule.apply(self.text, self.checklist, self.result)
        self.assertEqual(result, expected_result)
        self.assertEqual(checklist, expected_checklist)


class TestForkRule(unittest.TestCase):
    def setUp(self):
        self.fork_rule = ForkRule(name='Test Fork')
        self.text = 'This is a test text with amounts 100,000 and 160,500.'
        self.checklist = [('Вознаграждение', 'OK')]
        self.result = True

    def test_apply(self):
        expected_result = False
        expected_checklist = [('Вознаграждение', 'OK'), ('Test Fork', 'X')]
        result, checklist = self.fork_rule.apply(self.text, self.checklist, self.result)
        self.assertEqual(result, expected_result)
        self.assertEqual(checklist, expected_checklist)