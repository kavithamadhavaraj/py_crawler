import unittest
import sys
sys.path.append('../')
from spider.html_page_retriever import HTMLPageRetriever
from spider.sitemap_retriever import SiteMapRetriever
from spider.retriever import Retriever


class PageRetrieverTest(unittest.TestCase):

    def test_domain_cleanup(self):
        pr = Retriever(2)
        self.assertEqual(pr.same_domain_cleanup("http://www.xyz.com/profile",'./create'), 'http://www.xyz.com/profile/create')
        self.assertEqual(pr.same_domain_cleanup("http://www.xyz.com/profile",'/update'), 'http://www.xyz.com/update')
        self.assertEqual(pr.same_domain_cleanup("http://www.xyz.com/profile",'#update'), None)
        
if __name__ == '__main__':
    unittest.main()