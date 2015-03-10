class TimeoutError(Exception):
    pass


class MangaDownloadError(Exception):
    def __init__(self, message, args=None):
        self.message = message
        super(MangaDownloadError, self).__init__(message, args)


class PageDownloadError(MangaDownloadError):
    def __init__(self, image_url, download_path):
        self.url = image_url
        self.path = download_path
        self.message = '{0} Page failed to download.'.format(self.url)
        super(PageDownloadError, self).__init__(self.message)

    def __repr__(self):
        return '{0} Page failed to download.'.format(self.url)

class RequestError(MangaDownloadError):
    def __init__(self, message, *args):
        self.message = message
        super(RequestError, self).__init__(self.message, args)

    def __repr__(self):
        return self.message