import utils
import logging
import exception
import os
import threading


class TaskManager(object):

    def __init__(self, downloader, max_threads=None):
        # Will later implement for case when user specifies the max number of threads
        # for managing chapter task.
        # Temporarlily it will work for only max_threads=None

        if max_threads:
            raise NotImplementedError('max_threads specification has not yet been implemented')
        self.downloader = downloader
        self.max_threads = max_threads

    def start_all_tasks(self):
        threads = []
        if self.max_threads is None:
            chapter = self.downloader.get_chapter_from_queue()
            while chapter:
                threads.append(Task(self.downloader, chapter))
                chapter = self.downloader.get_chapter_from_queue()

            for t in threads:
                t.start()


class Task(threading.Thread):
    num_threads = 0

    def __init__(self, downloader, chapter=None, name='Task'):
        super(Task, self).__init__()
        Task.num_threads += 1
        self.id = Task.num_threads
        self.downloader = downloader
        self.chapter = chapter
        self.name = name + '-' + str(self.id)
        self.daemon = True
        self.stoprequest = threading.Event()

    def join(self, timeout=None):
        self.stoprequest.set()
        super(Task, self).join(timeout)

    def run(self):
        logging.debug('Started thread: ' + super(Task, self).name)
        print('Started thread: ' + super(Task, self).name)

        chap_folder_name = '{0}.{1}'.format(self.chapter.number.zfill(4), utils.slugify(self.chapter.name))
        download_dir = os.path.join(self.downloader.download_dir, chap_folder_name)
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        try:
            self.downloader.add_chapter_pages_task(self.chapter, download_dir)
            logging.info('Added chapter pages to Queue for {0}'.format(self.chapter))
        except exception.MangaDownloadError as e:
            logging.error(e.message)
            self.downloader.add_failed(self.chapter)
            print e.message

        logging.info('Thread closed: ' + super(Task, self).name)
        print('Thread closed: ' + super(Task, self).name)
