from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import urllib
import newspaper
import json
import topics
import LDA
from os import curdir, path

PORT_NUMBER = 8080

sampleURLs = ['http://www.economist.com/news/leaders/21709951-his-victory-threatens-old-certainties-about-america-and-its-role-world-what-will-take', 'http://bigstory.ap.org/article/ad892a1a81e54fea863edb2a103f4fce/last-foreign-tour-obama-must-find-way-explain-trump', 'http://nypost.com/2016/11/11/new-york-times-we-blew-it-on-trump/']


lda = None
tf_vectorizer = None
transformed = None
corpus = open('news.tsv').read().split('\n')
newsURLs = open('newsurls.txt').read().split('\n')

class myHandler(BaseHTTPRequestHandler):
    # Handler for the GET requests
    def do_GET(self):
        self.send_response(200)

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
            
            text = article.text.replace('\n', ' ')
            similarArticleIndices = topics.getArticleTopicSK(text, lda, tf_vectorizer, transformed)
            response = []

            for index in similarArticleIndices:
                similarArticle = corpus[index]
                newsURL = newsURLs[index]
                responseArticle = newspaper.Article(url=newsURL, language='en')
                responseArticle.download()
                responseArticle.parse()
                response.append({'url': newsURL, 
                                 'source': 'CNN',
                                 'title': responseArticle.title, 
                                 'authors': responseArticle.authors,
                                 'content': similarArticle,
                                 'topImage': responseArticle.top_image})

            #topics.getKeyPhrases(article.text)

            # Send the html message
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            # Handle files
            if self.path == '/favicon.ico':
                return
            f = open(curdir + self.path, 'rb')
            print('Serving ' + curdir + self.path)
            filename, extension = path.splitext(self.path)
            if extension == '.css':
                self.send_header('Content-type', 'text/css')
            elif extension == '.js':
                self.send_header('Content-type', 'text/js')
            else:
                self.send_header('Content-type', 'text/html')
                
            self.end_headers()
            self.wfile.write(f.read())

try:
    (lda, tf_vectorizer, transformed) = LDA.getLDAModel()
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print('Started httpserver on port ', PORT_NUMBER)

    # Wait forever for incomin ghttp requests
    server.serve_forever()

except KeyboardInterrupt:
    print('^C received, shutting down the web server')
    server.socket.close()
