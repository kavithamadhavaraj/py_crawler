from utils import get_base_url, clean_url

class Retriever(object):
    def __init__(self, strict):
		self.strict_domain = strict

    def same_domain_cleanup(self, entry_url, url):
        #Do not parse the URL query string
        url = (url.split('?')[0]) if (url != None) else url 
        if url == '/':
            url = None
        elif url.startswith("mailto:"):
        #If its email links, ignore
            url = None
        #Same domain or relative URL cleanup and convertion into proper URL string
        elif url.startswith('/'):
            url = clean_url(get_base_url(entry_url)) + url
        elif url.startswith('./'):
            url = clean_url(entry_url) + clean_url(url.replace(".",""))
        elif url.startswith('#'):
            #Do not parse hyperlinks starting with #, since it redirects to the same page
            url = None
        return url
