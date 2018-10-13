import requests
from bs4 import BeautifulSoup

class PageRetriever(object):

    def __init__(self, timeout):
        if timeout > 0:
            self.timeout = timeout
        else:
            raise RuntimeError("Timeout value cannot be negative")

    def same_domain_cleanup(self, entry_url, url):
        #Same domain URL cleanup
        if url.startswith('/'):
            url = entry_url.rstrip("/")+ url
        elif url.startswith('./'):
            url = entry_url.rstrip("/")+'/'+ url.lstrip("./")
        return url

    def strip_parameters(self, url):
        #Ignore URL parameters
        url = url.split('?')[0]
        #If there is any space in the url, strip
        url = url.strip()
        return url

    def getLinks(self, entry_url):
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
        links = set([])
        try:
            #Wait for 3 seconds before raising Timeout exception
            page = requests.get(entry_url, timeout=self.timeout)
            mime_type = page.headers['content-type']
            #Do not parse other content-type pages eg. PDF, Image, Json links etc. 
            if 'text/html' not in mime_type:
                #Note: If the objective of the crawler is to mine images / documents, mining logic must go here..
                return None
            page.raise_for_status()
            bs = BeautifulSoup(page.text, 'lxml')
            for link in bs.find_all('a'):
                url = link.get('href')
                if url != None:
                    url = self.same_domain_cleanup(entry_url, url)
                    #To keep off the garbage links
                    if url.startswith('https://') | url.startswith('http://'):
                        url = self.strip_parameters(url)
                        if (url != None) and url != entry_url:
                            #Add to bucket
                            links.add(url)
            return links
        except requests.exceptions.ConnectionError as e:
            print "ERROR: Contacting "+ entry_url + ", URL might be incorrect" 
            return None
        except requests.exceptions.Timeout as e:
            print "ERROR: Contacting "+ entry_url + ", timeout error" 
            return None
        except requests.exceptions.RequestException as e:
            print "ERROR: Contacting "+ entry_url + ", " + e.message
            return None
