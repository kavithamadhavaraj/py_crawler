import sys
import time
import json
import Queue
import threading
import requests
from bs4 import BeautifulSoup
from html_page_retriever import HTMLPageRetriever
from sitemap_retriever import SiteMapRetriever
from utils import sanity_check, remove_protocol, clean_url


class Crawler(object):
    
    def __init__(self, url, url_count=None, timeout=3, multi=5, strict=False):
        if sanity_check(url, url_count, multi):
            self.crawler_queue = Queue.Queue()
            self.directory = {} #Directory structure of crawled links
            self.root = url
            self.url_count = url_count #Max number of pages to crawl            
            self.visits = set([]) #List of visited pages implemented in Set for faster lookups
            self.timeout = timeout #Timeout for the page requests
            self.strict = strict #Strictly crawls same domain urls
            self.multi = multi #Concurrent requests can happen
        else:
            return None

    def __str__(self):
        return self.directory.__str__()

    def save_directory(self, file_name, path='./'):
        """
        Save the crawled directory of links into a JSON file

        Parameters
        ----------

        file_name: string
            File name without extension

        path: string
            Default is current directory
        """ 
        print "Saving to file..."
        with open(path+'/'+file_name+'.json', 'w') as fp:
            json.dump(self.directory, fp, indent=4)
        print "Finished"
    
    def count_exceeded(self):
        #Returns a boolean value to show if the count exceeded
        return len(self.visits) >= self.url_count
    
    def set_maximum(self):
        #If the crawler is set to run until interruption, set the maximum url count to infinity
        self.url_count = float("inf")    
    
    def request(self, entry_url):
        try:
            #some santity checks
            if self.timeout < 0:
                raise ValueError("Timeout param can take only positive value")
            if type(self.strict) != type(True):
                raise ValueError("Strict param can take only boolean value")   
            entry_url = clean_url(entry_url)
            #Wait for some time before raising Timeout exception
            page = requests.get(entry_url, timeout=self.timeout)
            mime_type = page.headers['content-type']
            page.raise_for_status()
            #Stop if the no of pages visited is exceeded
            if self.count_exceeded():
                return
            if (page != None) and remove_protocol(entry_url) not in self.visits:
                #Add the page to the visits list
                self.visits.add(clean_url(remove_protocol(entry_url)))
                soup = BeautifulSoup(page.text, 'lxml')      
                if 'text/html' in mime_type:  
                    #If the page is HTML delegate it to HTMLPageRetriever
                    pr = HTMLPageRetriever(self.strict)
                    pr.add_links(self.crawler_queue, self.directory, entry_url, soup)
                elif 'text/xml' in mime_type:
                    #If the page is XML delegate it to SiteMapRetriever
                    sr = SiteMapRetriever(self.strict)
                    sr.add_links(self.crawler_queue, self.directory, entry_url, soup)
                else:
                    return 
                print "--> " + entry_url
                return
        except requests.exceptions.ConnectionError as e:
            self.visits.add(clean_url(remove_protocol(entry_url)))
            print "Ignoring "+ entry_url + ", URL might be incorrect" 
            return None
        except requests.exceptions.Timeout as e:
            self.visits.add(clean_url(remove_protocol(entry_url)))
            print "Ignoring "+ entry_url + ", timeout error" 
            return None
        except requests.exceptions.RequestException as e:
            self.visits.add(clean_url(remove_protocol(entry_url)))
            print "Ignoring: "+ entry_url + ", " + e.message
            return None
        except RuntimeError as e:
            print e
            return None

    def process(self):
        try:
            if self.url_count == None:
                self.set_maximum()

            #Process until interrupted / count is matched
            while True:
                #Limit the number of threads to the user specified value
                #enumerate always return the child threads along with the main thread, ignore the later
                if (len(threading.enumerate())-1) < self.multi:
                    #If count is exceeding, break the process
                    if self.count_exceeded():
                        break 
                    #Wait until a mintue, to retrieve from queue
                    page = clean_url(self.crawler_queue.get(block=True, timeout=self.timeout))
                    # If node hasn't been visited yet, proceed
                    if remove_protocol(page) not in self.visits:
                        try:
                            #Collect URL's from the page
                            threading.Thread(target=self.request, args=[page]).start()
                        except Exception as e:
                            print e.message
                            break
                else:
                    #Give some time for the threads to finish, since we should restrict the threads being spawned to the user-specified value
                    time.sleep(2)
            
        except KeyboardInterrupt as e:
            print '\n\n---------------------------'
            print "\nFinishing the running jobs..."
            print '\n-----------------------------'
        except Queue.Empty as e:
            print "\nDone.."
        except ValueError as e:
            print e.message
        finally:
            #Join all existing threads to main thread.
            for thread in threading.enumerate():
                if thread is not threading.currentThread():
                    thread.join(self.timeout)
        return self.directory

    def engage(self):
        print "\nCrawler engaged"
        print "-"*20
        #Initiate the crawler, by placing the first URL in the processing queue
        self.crawler_queue.put(clean_url(self.root))
        return self.process()
    
    


