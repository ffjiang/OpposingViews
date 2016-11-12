from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import urllib
import newspaper
import json

PORT_NUMBER = 8080

sampleURLs = ['http://www.economist.com/news/leaders/21709951-his-victory-threatens-old-certainties-about-america-and-its-role-world-what-will-take', 'http://bigstory.ap.org/article/ad892a1a81e54fea863edb2a103f4fce/last-foreign-tour-obama-must-find-way-explain-trump', 'http://nypost.com/2016/11/11/new-york-times-we-blew-it-on-trump/']

class myHandler(BaseHTTPRequestHandler):
    # Handler for the GET requests
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        queryComponents = parse_qs(urlparse(self.path).query)

        if len(queryComponents) > 0:
            articleURL = urllib.parse.unquote(queryComponents["article"][0])
            print(articleURL)
            article = newspaper.Article(url=articleURL, language='en')


            '''
            cnn = newspaper.build('http://edition.cnn.com/')
            for article in cnn.articles:
                print(article.url)
            '''

            article.download()
            article.parse()
            
            response = []
            for url in sampleURLs:
                responseArticle = newspaper.Article(url=url, language='en')
                responseArticle.download()
                responseArticle.parse()
                response.append({'url': url, 'title': responseArticle.title, 
                                 'content': responseArticle.text})


            # Send the html message
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.wfile.write(bytes("Pass an article URL", 'utf-8'))
        return

try:
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print('Started httpserver on port ', PORT_NUMBER)

    # Wait forever for incomin ghttp requests
    server.serve_forever()

except KeyboardInterrupt:
    print('^C received, shutting down the web server')
    server.socket.close()
