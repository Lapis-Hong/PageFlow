# PageFLow
*PageFlow* is a Python (2 and 3) library for webpage search result crawler. 
It provides a simple API and support Google, Baidu, Bing search engines.
[https://pypi.org/project/pageflow/]

## Features
- support pages argument instead of just the first pate result.
- support redirect pages information extraction.


## Installation
### 1. using pip
```shell
pip install pageflow
```
### 2. using setup.py
``` shell
git clone https://github.com/Lapis-Hong/PageFlow.git 
cd PageFlow
pip setup.py install
```

## Usage
```python
from pageflow import PageFlow

query = "python"
pages = 1  # search results total pages

pf = PageFlow("baidu", proxies=None)


# Get search page html.
html = pf.get_html(query=query, pages=pages)


# The following results are all generator of SearchResult obj.
# Get search result urls.
url = pf.get_url(query=query, pages=pages)

# Get search result titles.
title = pf.get_title(query=query, pages=pages)

# Get search result abstract.
abstract = pf.get_abstract(query=query, pages=pages)

# Get search result redirect html.
redirect_html = pf.get_redirect_html(query=query, pages=pages)

# Get search result redirect content.
redirect_content = pf.get_redirect_content(query=query, pages=pages)

# Get search result title, abstract and url.
result = pf.get(query=query, pages=pages)

# Get search result title, abstract, url, redirect html and redirect content.
result_all = pf.get_all(query=query, pages=pages)
```

## References
https://github.com/howie6879/magic_google 
https://github.com/meibenjin/GoogleSearchCrawler  
https://github.com/chrislinan/cx-extractor-python 






