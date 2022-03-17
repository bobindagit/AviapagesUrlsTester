import unittest
from analyzer import Analyzer
import parser
import analyzer


class AnalyzerTest(unittest.TestCase):
    def test_get_word_list(self):
        analyzer.download_nltk_data()
        text = 'UUWW - EVRA 2Pax Challenger 300'
        answer = ['UUWW', 'EVRA', '2Pax', 'Challenger']
        self.assertEqual(Analyzer.get_words_list(text), answer)
        text = 'I love Python so much. My repositories are located at https://github.com/'
        answer = ['love', 'Python', 'much', 'repository', 'locate']
        self.assertEqual(Analyzer.get_words_list(text), answer)
        text = 'My phone number is +(373) 767 411 41'
        answer = ['phone', 'number']
        self.assertEqual(Analyzer.get_words_list(text), answer)


if __name__ == '__main__':
    unittest.main()
