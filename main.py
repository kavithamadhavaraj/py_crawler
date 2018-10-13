"""
Developer : Kavitha Madhavaraj

To interrupt do any of the following:
    * Press Enter twice
    * Use ctrl+c 
    * Any key/s followed by Enter

"""
from spider.crawler import Crawler

#Case 1: Specify the number of URL's to crawl 
cr1 = Crawler('http://www.windowscentral.com/', 5)
directory =  cr1.engage()

print "\n\nPages visited (Case1) : ", len(cr1.visits)
#Save the crawled directory in a JSON file
cr1.save_directory('Result1')

#Case 2: Crawl untill interrupted (ctrl+c)
cr2 = Crawler('http://www.windowscentral.com/')
directory =  cr2.engage()
print "\n\nPages visited (Case2) : ", len(cr2.visits)

#Save the crawled directory in a JSON file
cr2.save_directory('Result2')


