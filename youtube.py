import logging

from . import HTMLView
import homeassistant.core as ha

from youtube_dl import YoutubeDL
from youtube_dl.utils import DownloadError, ExtractorError

URL = 'https://www.youtube.com/playlist?list='
#URL = 'https://www.youtube.com/playlist?list=UUv5dc2Zi6j5IXQ_NKTZuSLA'
#URL = 'https://www.youtube.com/playlist?list=UUUYdl0nS0uA0cQ64LnDupRA'

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
    url = '/my_api/youtube/{path:.*}'
    name = 'my_api:youtube'
    requires_auth = False

    @ha.callback
    def get(self, request, path):
        msg = ''
        status = 200

        try:
            ydl = YoutubeDL({'quiet': True, 'playlist_items': '1-10', 'logger': _LOGGER})

            msg = '<html><head><meta charset="utf-8"/></head><body>'

            url = URL + path
            _LOGGER.debug(url)
            playlist = ydl.extract_info(url, process=True, download=False)
            entries = playlist['entries']
            for entry in entries:
#                print(entry['title'])
#                print(entry['upload_date'])
                for format in entry['formats']:
                    if format['format_id'] == '18':
#                        print(format['url'])
                         msg = msg + '<a href="{}">{} {}</a><br>'.format(format['url'], entry['upload_date'], entry['title'])

            msg = msg = msg + '</html></body>'
        except Exception as e:
            msg = '<html><body>{}</body></html>'.format(e)
            status = 404

        return self.html(msg, status)

if __name__ == '__main__':
    ydl = YoutubeDL({'quiet': True, 'playlist_items': '1-3', 'logger': _LOGGER})

    try:
        playlist = ydl.extract_info(URL, process=True, download=False)
#        print(playlist)
        entries = playlist['entries']
        for entry in entries:
#            print(entry)
            print(entry['title'])
            print(entry['upload_date'])
            for format in entry['formats']:
                if format['format_id'] == '140':
                    print(format['url'])
#        m = [next(entries) for _ in range(5)]
#        for i in m:
#            print(i)
#            print(i['title'], i['url'])
#            v = ydl.extract_info(i['url'], process=False, download=False)
#            print(v)
    except Exception as e:
        print('Exception')
        print(e)
