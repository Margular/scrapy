# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.files import FilesPipeline

import functools
import hashlib
import os
import os.path
import time
import logging
from email.utils import parsedate_tz, mktime_tz
from six.moves.urllib.parse import urlparse
from collections import defaultdict
import six

try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

from twisted.internet import defer, threads

from scrapy.pipelines.media import MediaPipeline
from scrapy.settings import Settings
from scrapy.exceptions import NotConfigured, IgnoreRequest
from scrapy.http import Request
from scrapy.utils.misc import md5sum
from scrapy.utils.log import failure_to_exc_info
from scrapy.utils.python import to_bytes
from scrapy.utils.request import referer_str
from scrapy.utils.boto import is_botocore
from scrapy.utils.datatypes import CaselessDict

logger = logging.getLogger(__name__)

class VideoPipeline(object):
    def process_item(self, item, spider):
        return item

class MyFilesPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None):
        ## start of deprecation warning block (can be removed in the future)
        def _warn():
            from scrapy.exceptions import ScrapyDeprecationWarning
            import warnings
            warnings.warn('FilesPipeline.file_key(url) method is deprecated, please use '
                          'file_path(request, response=None, info=None) instead',
                          category=ScrapyDeprecationWarning, stacklevel=1)

        # check if called from file_key with url as first argument
        if not isinstance(request, Request):
            _warn()
            url = request
        else:
            url = request.url

        # detect if file_key() method has been overridden
        if not hasattr(self.file_key, '_base'):
            _warn()
            return self.file_key(url)
        ## end of deprecation warning block

        media_guid = hashlib.sha1(to_bytes(url)).hexdigest()  # change to request.url after deprecation
        print("media_guid : %s" % media_guid)
        media_ext = os.path.splitext(url)[1].split('?')[0]  # change to request.url after deprecation
        print("media_ext : %s" % media_ext)
        return 'full/%s%s' % (media_guid, media_ext)
