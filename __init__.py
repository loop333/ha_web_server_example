#import asyncio
#import logging

#import urllib.request
#import urllib.parse
#import xml.etree.ElementTree as ET
#import re

from aiohttp import web
#import voluptuous as vol

from homeassistant.components.http import HomeAssistantView
#import homeassistant.core as ha

#_LOGGER = logging.getLogger(__name__)

DOMAIN = 'my_api'
DEPENDENCIES = ['http']

class HTMLView(HomeAssistantView):

    def html(self, body, status=200, headers=None):
        response = web.Response(body=body,
                                content_type='text/html',
                                status=status,
                                headers=headers)
        response.enable_compression()

        return response

def setup(hass, config):
    from .youtube import youtube
    from .tvpassport import tvpassport
    from .cnn import cnn

    hass.http.register_view(tvpassport)
    hass.http.register_view(cnn)
    hass.http.register_view(youtube)

    return True
