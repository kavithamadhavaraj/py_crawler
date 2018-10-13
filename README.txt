
To install the dependencies : 
	>> pip install -r requirements.txt

To run the test cases:
	>> python -m unittest discover -v

To run the main / driver program:
	>> python main.py


Modules
*******
 -crawler 
	Contains the core Crawler module
 -retreiver
	Contains PageRetriever, which retrieves the pages from web as instructed by Crawler
 -utils
	Includes some helper functions


Approach
********

There are two ways to run this crawler. 

- Specify how many pages to crawl
 	cr1 = Crawler('http://www.windowscentral.com/', 5)

- Crawl until interrupted
	cr2 = Crawler('http://www.windowscentral.com/')
	
	To interrupt do any of the following:
	    * Press Enter twice
	    * Use ctrl+c 
	    * Any key/s followed by Enter

- Once the crawler is engaged, the initial url is placed in Queue and the crawling process is initiated.

- This process runs until the number of pages crawled matches with the input (Case 1) / there is nothing left in the processing queue (Case2)

- When a url obtained from queue is visited, it is checked for mime-type to be html otherwise ignored (eg. pdf / images etc). 

- Timeout interval can be configured to give enough time for the retreiver. Default is 3 seconds

- If there is any Timeout / HTTP error etc occurs during the visit, the page is ignored and the process continues with the next link from queue.

- For all the child urls found in the page, following process are done
	- same domain links that start with / or ./ are converted into proper format
	- url parameters are ignored
	- duplicates are removed

- Once a link is crawled, it is marked as visited. So that it isn't processed again when the same link occurs in any other pages.

- The mapping of pages and their child urls, known as directory is maintained through out the crawling process and is available as a JSON file.






