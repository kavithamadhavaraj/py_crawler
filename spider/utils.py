from urlparse import urlparse

def sanity_check(data, url_count, multi):
    #Some preliminary checks to create Crawler object
    if (url_count != None) & (url_count <= 0):
        raise RuntimeError("url_count param can have values from 1 - N" )
    elif (data == None) or (not url_valid(data)):
        raise RuntimeError("url param can accept only valid URL's" )
    elif (multi != None) & (multi <= 0):
        raise RuntimeError("multi param can have values from 1 - N" )
    else:
        return True  

def url_valid(url):
    #Check if the provided URL is valid eg. www.abc is not a valid URL
    try:
        result = urlparse(url)
        return ((result.scheme != '') & (result.netloc != ''))
    except:
        return False

def get_base_url(url):
    #Find the scheme & hostname of any URL 
    #Eg: https://www.google.com/profile/abc return https://wwwo.google.com
    try:
        url_block = urlparse(url)
        base_url = url_block.scheme + "://" + url_block.hostname
        return base_url
    except:
        return None

def remove_protocol(url):
    #Remove the following tokens from URL string
    replace_tokens = ["https://", "http://",'www.']
    for token in replace_tokens:
        url = url.replace(token,'')
    return url

def clean_url(url, leading=False):
    #Strip the characters like / or # from URL string, if leading is True.
    #Removes both the leading and trailing characters
    if leading == True:
        return url.strip('#').strip('/').strip()
    else:
        return url.rstrip('#').rstrip('/').strip()
