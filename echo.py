import logging

import urllib.request
import re
import json

from . import HTMLView
import homeassistant.core as ha

_LOGGER = logging.getLogger(__name__)

class echo(HTMLView):

    url = '/my_api/news/echo'
    name = 'my_api:news_echo'
    requires_auth = False

    @ha.callback
    def get(self, request):
        status = 200
        try:
            resp = urllib.request.urlopen('https://echo.msk.ru/api/news.json?fields=title,body,url')
            t = json.load(resp)
            news = t['content']

            msg = ''
            msg = msg + '<html>\n'
            msg = msg + '<head>\n'
            msg = msg + '<meta charset="utf-8"/>\n'
            msg = msg + '<style>\n'
            msg = msg + 'div,a {\n'
            msg = msg + ' margin-left: 30px;\n'
            msg = msg + '}\n'
            msg = msg + '</style>\n'
            msg = msg + '</head>\n'
            msg = msg + '<body>\n'
            for n in news:
                title = n['title']
                title = re.sub(r' +', ' ', title)
                title = re.sub(r'^ +', '', title)
                body = n['body']
                body = re.sub(r' +', ' ', body)
                body = re.sub(r'^ +', '', body)
                msg = msg + '<details>\n'
                msg = msg + '<summary>{}</summary>\n'.format(title)
                msg = msg + '<div>{}</div>\n'.format(body)
                msg = msg + '<a href="{}">More</a>'.format('https://echo.msk.ru'+n['url'])
                msg = msg + '</details>\n'
            msg = msg + '</body>\n'
            msg = msg + '</html>\n'

        except:
            msg = '<html><body>Error</body></html>'
            status = 404

        return self.html(msg, status)
