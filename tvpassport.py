import logging

import urllib.request
import urllib.parse
import re

from . import HTMLView
import homeassistant.core as ha

_LOGGER = logging.getLogger(__name__)

class tvpassport(HTMLView):

    url = '/my_api/tvpassport/{path:.*}'
    name = 'my_api:tvpassport'
    requires_auth = False

    @ha.callback
    def get(self, request, path):
        data = {'timezone': 'Asia/Yekaterinburg'}
        data = urllib.parse.urlencode(data).encode('utf-8')
        req = urllib.request.Request('https://www.tvpassport.com/my-passport/dashboard/save_timezone', data=data)
        resp = urllib.request.urlopen(req)
        cisession = None
        for c in resp.info().get_all('Set-Cookie'):
            m = re.match(r'cisession=(.*?);', c)
            if m: cisession = m[1]

        status = 200
        try:
            req = urllib.request.Request('https://www.tvpassport.com/tv-listings/stations/' + path)
            if cisession:
                req.add_header('Cookie', 'cisession=' + cisession)
            resp = urllib.request.urlopen(req)
            d = resp.read().decode('utf-8')

            m = re.search(r'<title>TV Schedule for (.*?) | TV Passport</title>', d)
            station = m[1]
            m = re.search(r'<option value="([^"]*)" selected>', d)
            timezone = m[1]

            msg = '<html><head><title>{}</title></head><body>'.format(station)
            msg = msg + '<table>'
            for i in re.findall(r'<div id="itemheader.*?>', d):
                sched = {}
                for type, value in re.findall(r'([^ "=]+)="(.*?)"', i):
                    if value:
                        sched[type] = value
                msg = msg + '<tr><td>{}<td>{}'.format(sched['data-st'], sched['data-showName'])

            msg = msg + '</table>'
            msg = msg + '</body></html>'
        except:
            msg = '<html><body>Error</body></html>'
            status = 404

        return self.html(msg, status)
