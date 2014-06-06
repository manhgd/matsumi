from handler.base import Handler
import http.client
import tornado.escape
import re

class Page(Handler):
    def get(self, page):
        if not page:
            page = 'home'
        self.render(page + '.html')
        
class Gloss(Handler):
    WWWJDICT = {
        'host': 'www.csse.monash.edu.au',
        'path': '/~jwb/cgi-bin/wwwjdic.cgi?9ZIG'
    }
    def get(self):
        self.render('gloss.html')
        
    def post(self):
        conn = http.client.HTTPConnection(self.WWWJDICT['host'])
        text = self.get_argument('text')
        conn.request('GET', self.WWWJDICT['path'] + tornado.escape.url_escape(text))
        res = conn.getresponse()
        html = res.read().decode('utf-8')
        matched = re.search(r"""<body>(.+)</body>""", html, re.DOTALL + re.IGNORECASE + re.MULTILINE)
        if matched:
            body_html = matched.group(0)
            self.write(body_html)
        else:
            self.write("Bad result")