import thread, time
from retriever import PageRetriever
from utils import interruption_handler, sanity_check
import sys
import Queue
import json

class Crawler(object):
    def __init__(self, url, url_count = None, time_out=3):
        if sanity_check(url, url_count):
            self.root = url
            self.url_count = url_count #Max number of pages to crawl
            self.crawler_queue = Queue.Queue()
            self.directory = {} #Directory structure of crawled links
            self.visits = [] #List of visited pages
            self.retriever = PageRetriever(timeout= time_out)
            self.interruption_flag = []
        else:
            return None

    def __str__(self):
        return self.directory.__str__()

    def save_directory(self, filename, path='./'):
        """
        Save the crawled directory of links into a JSON file

        Parameters
        ----------

        filename: string
            File name without extension

        path: string
            Default is current directory
        """ 
        with open(path+'/'+filename+'.json', 'w') as fp:
            json.dump(self.directory, fp, indent=4)
    
    def prepare_for_interruption(self):
        #Create a thread that monitors the interruption
        thread.start_new_thread(interruption_handler, (self.interruption_flag,))

    def is_interrupted(self):
        return len(self.interruption_flag) > 0

    def register_visit(self, page):
        #Adds a visited page to the list, to be shown to user
        self.visits.append(page)

    def enque_pages(self, page_set):
        #Enque all the collected urls, to be processed one by one
        if page_set == None:
            return
        for link in page_set:
            self.crawler_queue.put(link)

    def register_directory(self, page, page_set):
        #Register a page, along with it's child URL's, to be shown / saved as file
        if page_set == None:
            return
        self.directory[page].extend(page_set)

    def count_exceeded(self):
        return len(self.visits) >= self.url_count
    
    def set_maximum(self):
        #If the crawler is set to run untill interruption, set the maximum url count to infinity
        self.url_count = float("inf")    

    def process(self):
        try:
            self.prepare_for_interruption()
            #Process untill the queue is empty
            while not self.crawler_queue.empty():               
                node = self.crawler_queue.get()
                # If node hasn't been visited yet, proceed
                if node not in self.visits:
                    print "-->", node
                    self.directory[node] = []                    
                    if self.url_count == None:
                        self.set_maximum()
                    if self.is_interrupted():
                        break
                    #Wait one second before every request
                    time.sleep(1)
                    #Collect URL's from the page
                    linkset = self.retriever.getLinks(node)
                    #Register the node as visited
                    self.register_visit(node)
                    #Load all the child URLs for further processing
                    self.enque_pages(linkset)
                    #Save the page and their child mapping
                    self.register_directory(node, linkset)
                    #If count is exceeding, break the process 
                    if self.count_exceeded():
                        break
        except KeyboardInterrupt as e:
            print "\nExiting please wait....."
        return self.directory

    def engage(self):
        print "\nCrawler engaged"
        print "-"*20
        #Initiate the crawler, by placing the first URL in the processing queue
        self.crawler_queue.put(self.root)
        return self.process()

