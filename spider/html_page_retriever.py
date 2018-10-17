from retriever import Retriever
from utils import get_base_url, clean_url


class HTMLPageRetriever(Retriever):
    
    def __init__(self, strict):
        super(HTMLPageRetriever, self).__init__(strict)

    def add_links(self, process_queue, directory, entry_url, soup):
        """
        Extract the valid links from the provided URL

        Parameters
        ----------

        process_queue: Queue

        directory: dictionary
            Dictionary to store the parent and child url mappings

        entry_url: string
            URL to extract the hyperlinks

        soup : BeautifulSoup extract            
        
        """ 
        
        link_set = soup.find_all('a', href=True)
        directory[entry_url] = set([])
        for link in link_set:
            #Find the urls from the soup extract and clean them for relative paths
            url = self.same_domain_cleanup(entry_url, link.get('href'))
            #If strict flag is set, ignore the url from other domains
            if ((self.strict_domain == True) and (get_base_url(url) != get_base_url(entry_url))):
                continue
            if (url != None)  and (url != '') and (url != entry_url):
                #Load all the child URLs for further processing
                process_queue.put(clean_url(url))
                #Register a page, along with it's child URL's, to be shown / saved as file
                directory[entry_url].add(url)
        #Converting set into list for serialising    
        directory[entry_url] = list(directory[entry_url])
