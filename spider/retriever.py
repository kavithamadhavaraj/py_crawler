import requests
from bs4 import BeautifulSoup
from utils import get_base_url, clean_url

class PageRetriever(object):

    def __init__(self, timeout):
        if timeout > 0:
            self.timeout = timeout
        else:
            raise RuntimeError("Timeout value cannot be negative")

    def same_domain_cleanup(self, entry_url, url):
        #Same domain URL cleanup
        if url.startswith('/'):
            url = clean_url(get_base_url(entry_url)) + clean_url(url)
        elif url.startswith('./'):
            url = clean_url(entry_url) + clean_url(url.replace(".",""))
        elif url.startswith('#'):
            #Do not parse hyperlinks starting with #, since it redirects to the same page
            url = None
        return url

    def strip_parameters(self, url):
        #Ignore URL parameters
        url = clean_url(url.split('?')[0])
        return url

    def get_links(self, entry_url):
        """
        Extract the valid links from the provided URL

        Parameters
        ----------

        entry_url: string
            URL to extract the hyperlinks

        Returns
        -------
        List of valid hyperlinks
        """ 
        
        try:
            entry_url = clean_url(entry_url)
            links = set([])
            #Wait for 3 seconds before raising Timeout exception
            page = requests.get(entry_url, timeout=self.timeout)
            mime_type = page.headers['content-type']
            #Do not parse other content-type pages eg. PDF, Image, Json links etc. 
            if 'text/html' not in mime_type:
                #Note: If the objective of the crawler is to mine images / documents, mining logic must go here..
                return None
            page.raise_for_status()
            print "-->", entry_url
            bs = BeautifulSoup(page.text, 'lxml')
            for link in bs.find_all('a'):
                href = link.get('href')
                if href != None:
                    url = self.same_domain_cleanup(entry_url, href)
                    #To keep off the garbage links
                    if ((url != None) and ( url.startswith('https://') | url.startswith('http://'))):
                        url = self.strip_parameters(url)
                        if (url != None) and (url != entry_url):
                            #Add to bucket
                            links.add(url)
            if links:
                return links
            else:
                return None
        except requests.exceptions.ConnectionError as e:
            print "ERROR: Contacting "+ entry_url + ", URL might be incorrect" 
            return None
        except requests.exceptions.Timeout as e:
            print "ERROR: Contacting "+ entry_url + ", timeout error" 
            return None
        except requests.exceptions.RequestException as e:
            print "ERROR: Contacting "+ entry_url + ", " + e.message
            return None
