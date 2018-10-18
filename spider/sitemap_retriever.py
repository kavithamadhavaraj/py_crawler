from retriever import Retriever
from utils import get_base_url, clean_url, remove_protocol

class SiteMapRetriever(Retriever):

    def __init__(self, strict):
        super(SiteMapRetriever, self).__init__(strict)
    
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
        link_set = soup.find_all("url")
        #If there is no url tag found in XML file, it is not a sitemap / malformed
        if link_set == None:
            raise RuntimeWarning("malformed sitemap")

        directory[entry_url] = set()
        domain = remove_protocol(get_base_url(entry_url))

        for link in link_set:
            #Find the url tags from XML and clean them for relative paths
            link = link.findNext("loc")
            if link != None:
                url = self.same_domain_cleanup(entry_url, link.text)
                if (url != None):
                    #If strict flag is set, ignore the url from other domains
                    if (self.strict_domain == True): 
                        if (remove_protocol(get_base_url(url)) != domain):
                            continue
                    if (url != entry_url):
                        #Load all the child URLs for further processing
                        process_queue.put(clean_url(url))
                        #Register a page, along with it's child URL's, to be shown / saved as file
                        directory[entry_url].add(url)
        if link_set == None:
            raise RuntimeError("Ignoring "+ entry_url + ", malformed xml/sitemap")
        #Converting set into list for serialising    
        directory[entry_url] = list(directory[entry_url])
        

