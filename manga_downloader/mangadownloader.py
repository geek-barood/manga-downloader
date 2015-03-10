import Queue
import threading


class MangaDownloader(object):
    def __init__(self, name=None, url=None, download_dir=None):
        self.name = name
        self.url = url
        self.download_dir = download_dir
        self.task_queue = None
        self.chapters_to_download = None
        self.pages = []
        self.pages_done = 0
        self.failed = []
        self.chapters = None
        self._stop_request = threading.Event()
        self._stop_request.clear()
        self.task_queue = Queue.Queue()
        self.chapters_to_download = Queue.Queue()

    def got_stop_request(self):
        return self._stop_request.isSet()

    def set_stop_request(self):
        self._stop_request.set()

    def add_failed(self, item):
        self.failed.append(item)

    def add_page_to_queue(self, page):
        self.task_queue.put(page)

    def set_url(self, url):
        self.url = url

    def set_download_dir(self, download_dir):
        self.download_dir = download_dir

    def set_name(self, name):
        self.name = name

    def get_chapter_from_queue(self):
        try:
            chapter = self.chapters_to_download.get(block=False)
        except Queue.Empty:
            return None
        self.chapters_to_download.task_done()
        return chapter

    def add_chapter_to_queue(self, chapter):
        self.chapters_to_download.put(chapter)

    def fetch_chapters(self):
        raise NotImplementedError

    def add_chapter_pages_task(self, chapter, download_dir):
        raise NotImplementedError
