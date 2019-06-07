# coding: utf-8
from __future__ import unicode_literals

import re

from .common import InfoExtractor

from ..utils import (
    extract_attributes,
    str_to_int,
)


class VPornIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?vporn\.com/.*?/.*?/(?P<id>[0-9]+)'
    _TEST = {
        'url': 'https://www.vporn.com/ebony/jdt-video/1319022/',
        'md5': 'f30a4476ef226dbb317e23822168ed1e',
        'info_dict': {
            'id': '1319022',
            'ext': 'mp4',
            'title': 'Jdt Video #60',
            'description': 'Nyomi Banxxx & Skin Diamond-Scene',
            'uploader': 'JonDoeTurdz',
            'uploader_id': '2474178',
            'thumbnail': r're:^https?://.*\.jpg$',
            'duration': 1689,
            'views': int,
            'age_limit': 18,
        }
    }

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)

        title = self._html_search_regex(r'<h1>(.+?)</h1>', webpage, 'title')

        uploader = self._html_search_regex(
            r'avatarname["\']>(.+?)</span>', webpage, 'uploader')

        uploader_id = self._search_regex(
            r'data-user=[\'"](\d+)[\'"]', webpage, 'uploader_id')

        thumbnail = self._search_regex(
            r'posterurl\s+=\s+[\'\"](.*?)[\'\"];', webpage, 'thumbnail')

        formats = []
        for source in re.findall(r'(<source[^>]+>)', webpage):
            attrs = extract_attributes(source)
            formats.append({'url': attrs.get('src'),
                            'height': int(attrs.get('res'))})
        self._sort_formats(formats)

        duration = int(self._search_regex(
            r'videoLength\s+=\s+(\d+?);', webpage, 'duration'))

        views = self._search_regex(
            r'(?s)view-count["\']>(.*?)views', webpage, 'views'
        ).strip()
        views = str_to_int(views)

        return {
            'id': video_id,
            'title': title,
            'formats': formats,
            'description': self._html_search_meta(
                'description', webpage, 'description'),
            'uploader': uploader,
            'uploader_id': uploader_id,
            'thumbnail': thumbnail,
            'duration': duration,
            'views': views,
            'age_limit': 18,
        }
