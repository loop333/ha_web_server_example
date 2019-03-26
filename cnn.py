import logging

import urllib.request
import xml.etree.ElementTree as ET
import re

from . import HTMLView
import homeassistant.core as ha

_LOGGER = logging.getLogger(__name__)

class cnn(HTMLView):
    url = '/my_api/news/cnn/{path:.*}'
    name = 'my_api:news_cnn'
    requires_auth = False

    @ha.callback
    def get(self, request, path):
        msg = ''
        status = 200
        try:
            resp = urllib.request.urlopen('http://rss.cnn.com/rss/' + path)
            xml = ET.parse(resp)
            root = xml.getroot()

            msg = '<html>\n<head>\n<meta charset="utf-8">\n</head>\n<body>\n'
            msg = msg + '<style>\ndiv, a {\n margin-left: 30px;\n}\n</style>\n'
            for item in xml.findall('channel/item'):
                title = item.find('title')
                title_txt = title.text
                description = item.find('description')
                description_txt = ''
                if description is not None:
                    description_txt = description.text
                    description_txt = re.sub(r'<[^>]*>', '', description_txt)
                    description_txt = re.sub(r'\s{2,}', ' ', description_txt)
                link = item.find('link')
                link_txt = ''
                if link is not None:
                    link_txt = link.text
                msg = msg + '<details>\n' \
                            '<summary>{}</summary>\n' \
                            '<div>{}</div>\n' \
                            '<a href="{}">More</a>\n' \
                            '</details>\n'. \
                            format(title_txt, description_txt, link_txt)

            msg = msg + '</body>\n</html>\n'
            status = 200
        except Exception as e:
            msg = '<html><body>{}</body></html>'.format(e)
            status = 404

        return self.html(msg, status)
