from mangahere import MangaHere


class MangaFactory(object):
    manga_provider = {'mangahere': MangaHere()}

    def __init__(self):
        pass

    @staticmethod
    def get_instance(downloader, manga_url, download_dir):
        assert isinstance(downloader, str)
        assert isinstance(manga_url, str)
        assert isinstance(download_dir, str)
        try:
            ret = MangaFactory.manga_provider[downloader]
        except KeyError:
            raise ValueError('{} downloader not present'.format(downloader))
        else:
            ret.set_url(manga_url)
            ret.set_download_dir(download_dir)
            return ret
