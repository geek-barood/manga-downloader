from nose.tools import *
import os
from manga_downloader import utils


def test_download_image():
    test_image_url = 'http://z.mhcdn.net/store/manga/11566/011.0/compressed/h005.jpg'
    test_dump_path = os.path.join(os.getcwd(), 'test_page.jpeg')
    utils.download_image(test_image_url, test_dump_path)
    assert_equal(os.path.exists(test_dump_path), True)
    os.remove(test_dump_path)


def test_stream_download_image():
    test_image_url = 'http://z.mhcdn.net/store/manga/11566/011.0/compressed/h005.jpg'
    test_dump_path = os.path.join(os.getcwd(), 'test_page.jpeg')
    utils.download_image(test_image_url, test_dump_path)
    assert_equal(os.path.exists(test_dump_path), True)
    os.remove(test_dump_path)
