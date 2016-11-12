# OpposingViews

TODO:

1) Build chrome extension
2) AWS - Python Server to do scraping/serving data
3) Scraping - Python Library
4) Political ideology model - for now, just give news sources a particular
rating on the ideological spectrum
5) Topic model - to find similar articles - Microsoft Cognitive Services API

Stack:
Python server
Server will scrape once a day/manually

Client sends URL to server
Server will gets the text of URL, plugs into topic model to get similar
articles.
Server sends articles back to client
