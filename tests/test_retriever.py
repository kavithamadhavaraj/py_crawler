import unittest
import sys
sys.path.append('../')
from spider.retriever import PageRetriever

class PageRetrieverTest(unittest.TestCase):

    def test_negative_timeout(self):
        with self.assertRaises(RuntimeError):
            PageRetriever(-1)

    def test_strip_parameters(self):
        pr = PageRetriever(2)
        self.assertEqual(pr.strip_parameters("http://www.google.com?a=5"),'http://www.google.com')
    
    def test_domain_cleanup(self):
        pr = PageRetriever(2)
        self.assertEqual(pr.same_domain_cleanup("http://www.xyz.com/profile",'./create'), 'http://www.xyz.com/profile/create')
        self.assertEqual(pr.same_domain_cleanup("http://www.xyz.com/profile",'/update'), 'www.xyz.com/update')
        self.assertEqual(pr.same_domain_cleanup("http://www.xyz.com/profile",'#update'), None)
        
if __name__ == '__main__':
    unittest.main()