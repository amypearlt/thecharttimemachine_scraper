I used Scrapy, a Python framework for web crawling and scraping, in order to extract data from [The Chart Time Machine](https://www.charttimemachine.com), a web archive of 20th century UK singles charts.

To scrape **all** charts from the 20th century, use:

`scrapy crawl charts`

To scrape a specific year, use `year`:

`scrapy crawl charts -a year=1963`

To scrape a specific decade, use `decade`:

`scrapy crawl charts -a decade=1990`

To scrape a week beginning on a specific date, use `week`:

`scrapy crawl charts -a week=1982-05-14`

To scrape weekly charts within a specific date range, pass your start and end dates via `from_date` and `to_date`:\
Keep in mind that the furthest back you can go is `1952-11-14`, and the charts end at `1999-12-16`.

`scrapy crawl charts -a from_date=1969-01-12 -a to_date=1971-11-08`

To dump the scraped data to a CSV file, use the output command:\
JSON and XML formats can also be used to export data.

`scrapy crawl charts -O charts.csv`

Scrapy's HTTP cache is enabled, allowing previously downloaded webpages to be re-retrieved locally - it prevents redundant website requests, and reduces crawling time.\
Every record in the exported data should be unique, identified by the *week* and *position* columns in conjunction; each record represents a distinct chart entry.

## A brief definition of web crawling and web scraping

#### <ins>Web Crawler:</ins> An Internet bot that systematically browses the World Wide Web.

A web crawler starts with an initial list of URLs to visit, which are called *seeds*. When visiting these URLs, the crawler identifies all of the hyperlinks in the retrieved webpages, and adds them to the list of URLs to visit, called the *crawl frontier*. URLs from the frontier are recursively visited. 

#### <ins>Web Scraper:</ins> A process in which data is extracted from webpages and entered into a local database.

A web scraper parses a webpage's DOM and identifies the HTML elements which contain relevant data. The data is extracted and converted into a structured format.[^1]

## My web scraping process, via Scrapy

### 1. Identify a suitable website to scrape data from.

I had to choose a UK charts website (Weekly UK Top 100 Singles Charts) where web scraping is permissible, defined by their *robots.txt* file. This meant I was forced to choose from older, often outdated websites, but the structure of these websites were often simpler, and it would therefore be easier for me to identify CSS selectors which pointed to the desired data within the DOM.

### 2. Identify and collect URLs.

In order to access chart information on the website, the user must fill in a dropdown menu requiring a date range and a range of chart positions. Since the website exposes search criteria through their URL's query parameters, the process of iterating through each weekly chart was convenient; I constructed the URL's query for every week within the desired time frame. Every song in the chart list contains a link to the song's own webpage, containing information about the song's genre and other statistics; I followed these links for every song to extract these details.

### 3. Identify CSS selectors which contain the relevant data.

Using my browser's *Inspect Element* feature, I could view the HTML code of the webpage and determine the CSS selectors used to contain data such as the song name, the song's artist, the peak position of the song, and so on.[^2]

### 4. Choose a filetype to store the data.

I chose CSV as a standard format for storing data, making it convenient to export into spreadsheets or databases.

[^1]: https://oxylabs.io/blog/web-scraping
[^2]: https://docs.scrapy.org/en/latest/intro/tutorial.html