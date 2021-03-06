import unittest
import sys
sys.path.append('../')
from spider.crawler import Crawler

class CrawlerTest(unittest.TestCase):

    def test_output_count(self):
        self.crawler = Crawler("https://stackoverflow.com/questions", 5, timeout=10)
        self.crawler.engage()
        self.assertEqual(len(self.crawler.directory.keys()), 5)

    def test_visited_count(self):
        self.crawler = Crawler("https://stackoverflow.com/questions", 2)
        self.crawler.engage()
        self.assertEqual(len(self.crawler.visits), 2)

    def test_zero_url_count(self):
        with self.assertRaises(RuntimeError):
            self.crawler = Crawler("http://www.google.com", 0)

if __name__ == '__main__':
    unittest.main()