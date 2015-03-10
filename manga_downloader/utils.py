import model
import utils
import logging
import requests
import exception
from bs4 import BeautifulSoup, SoupStrainer
import bs4
import re
import unicodedata


def download_image(image_url, dump_path):
    """
    This method downloads the given image

    If download fails then it throws PageDownloadError exception
    """
    try:
        r = requests.get(image_url)
        if r.status_code == 200:
            sz = int(r.headers['content-length'])
            with open(dump_path, 'wb') as f:
                f.write(r.content)

            logging.debug(image_url + ' downloaded successfully')
            return sz
        else:
            logging.debug('Image was not found or server error!')
            raise exception.PageDownloadError(image_url, dump_path)

    except requests.exceptions.ConnectionError:
            logging.debug('Downloading page failed: {0}'.format(image_url))
            raise exception.PageDownloadError(image_url, dump_path)


def stream_download_image(image_url, dump_path, chunk=1024):
    """
    This method downloads the given image

    If download fails then it throws PageDownloadError exception
    """
    try:
        r = requests.get(image_url, stream=True)
        if r.status_code == 200:
            sz = int(r.headers['content-length'])
            with open(dump_path, 'wb') as f:
                # default small chunk size takes too much of CPU
                for chunk in r.iter_content(chunk_size=chunk):
                    f.write(chunk)

            logging.debug(image_url + ' downloaded successfully')
            return sz
        else:
            logging.debug('Image was not found or server error!')
            raise exception.PageDownloadError(image_url, dump_path)

    except requests.exceptions.ConnectionError:
            logging.debug('Downloading page failed: {0}'.format(image_url))
            raise exception.PageDownloadError(image_url, dump_path)


def slugify(value):
    """
    Converts to ASCII. Converts spaces to hyphens. Removes characters that
    aren't alphanumerics, underscores, or hyphens. Converts to lowercase.
    Also strips leading and trailing whitespace.
    """
    value = unicode(value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    return re.sub('[-\s]+', '-', value)
