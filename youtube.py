import logging

from . import HTMLView
import homeassistant.core as ha

from youtube_dl import YoutubeDL
from youtube_dl.utils import DownloadError, ExtractorError

REQUIREMENTS = ['youtube_dl']

URL = 'https://www.youtube.com'

class mylogger:
    def debug(self, format, *args):
        print('DEBUG: ' + format % args)
    def warning(self, format, *args):
        print('WARNING: ' + format % args)
    def error(self, format, *args):
        print('ERROR: ' + format % args)

if __name__ == '__main__':
    _LOGGER = mylogger()
else:
    _LOGGER = logging.getLogger(__name__)

class youtube(HTMLView):
    url = '/my_api/youtube'
    name = 'my_api:youtube'
    requires_auth = False

    @ha.callback
    def get(self, request):
        msg = ''
        status = 200

        try:
            u = request.query.get('u')
            c = request.query.get('c')
            p = request.query.get('p')
            v = request.query.get('v')
            f = request.query.get('f', '18')
            s = int(request.query.get('s', '1'))
            n = int(request.query.get('n', '10'))

            ydl = YoutubeDL({'quiet': True, 'playlist_items': '1-10', 'logger': _LOGGER})

            msg = msg + '<html>\n'
            msg = msg + '<head><meta charset="utf-8"/></head>\n'
            msg = msg + '<body>\n'

            if u is not None:
                url = '{}/user/{}'.format(URL, u)
            if c is not None:
                url = '{}/channel/{}'.format(URL, c)
            if p is not None:
                url = '{}/playlist?list={}'.format(URL, p)
            if v is not None:
                url = '{}/watch?v={}'.format(URL, v)

            _LOGGER.debug(url)

            info = ydl.extract_info(url, process=False, download=False)

            if info['extractor'] == 'youtube':
                for format in info['formats']:
                    if format['format_id'] == f:
                        msg = msg + '<video controls playsinline autoplay style="width: 100%;" src={}></video>\n'.format(format['url'])

            entries = None
            if info['extractor'] in ['youtube:user', 'youtube:channel']:
                info2 = ydl.extract_info(info['url'], process=False, download=False)
                entries = info2['entries']

            if info['extractor'] == 'youtube:playlist':
                entries = info['entries']

            if entries is not None:
                skip = [next(entries) for _ in range(s-1)]
                entries = [next(entries) for _ in range(n)]
                for entry in entries:
                    msg = msg + '<a href="/my_api/youtube?v={}&f={}">{}</a><br>\n'.format(entry['url'], f, entry['title'])

            msg = msg + '</body>\n'
            msg = msg + '</html>\n'
        except Exception as e:
            msg = '<html><body>{}</body></html>'.format(e)
            status = 404

        return self.html(msg, status)

if __name__ == '__main__':
    ydl = YoutubeDL({'quiet': True, 'playlist_items': '1-3', 'logger': _LOGGER})

    try:
        playlist = ydl.extract_info(URL+'<playlist_id>', process=True, download=False)
#        print(playlist)
        entries = playlist['entries']
        for entry in entries:
#            print(entry)
            print(entry['title'])
            print(entry['upload_date'])
            for format in entry['formats']:
                if format['format_id'] == '140':
                    print(format['url'])
    except Exception as e:
        print('Exception')
        print(e)
