"""
Developer : Kavitha Madhavaraj

To interrupt the program:
    * Use ctrl+c 
"""
from spider.crawler import Crawler

#Case 1: Specify the number of URL's to crawl 
cr1 = Crawler('http://www.windowscentral.com/', url_count=30, strict=False, timeout=5, multi=10)
directory =  cr1.engage()
print "\n\nPages visited (Case1) : ", len(cr1.visits)
#Save the crawled directory in a JSON file
cr1.save_directory('Result1')

"""
#Case 2: Crawl untill interrupted (ctrl+c)
cr2 = Crawler('http://www.bitsathy.ac.in/sitemap.xml', timeout=5, strict=True)
directory =  cr2.engage()
print "\n\nPages visited (Case2) : ", len(cr2.visits)

#Save the crawled directory in a JSON file
cr2.save_directory('Result2')
"""