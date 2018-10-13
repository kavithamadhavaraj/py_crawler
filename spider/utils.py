from urlparse import urlparse

def interruption_handler(interruption_flag):
    #Signal the thread when an interrupt is observed
    interruption_flag.append(raw_input())

def sanity_check(data, url_count):
    #Some preliminary checks to create Crawler object
    if (url_count != None) & (url_count <= 0):
        raise RuntimeError("url_count param can have values from 1 - N" )
    elif (data == None) or (not url_valid(data)):
        raise RuntimeError("url param can accept only valid URL's" )
    else:
        return True  

def url_valid(url):
    #Check if the provided URL is valid eg. www.abc is not a valid URL
    try:
        result = urlparse(url)
        return ((result.scheme != '') & (result.netloc != ''))
    except:
        return False

def get_base_URL(url):
    print urlparse(url).hostname
    return urlparse(url).hostname