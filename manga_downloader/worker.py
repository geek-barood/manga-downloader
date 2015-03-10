import threading
import utils
import exception
import logging
from threading import Lock
import Queue
import time
import timeit


class WorkerThreadPool(object):

    def __init__(self, downloader, num_threads=1):
        self.downloader = downloader
        self.num_threads = num_threads
        self.workers = []
        self.bytes_downloaded = 0
        self.lock = Lock()
        self.end_threads = threading.Event()
        self.end_threads.clear()

        for i in xrange(num_threads):
            self.workers.append(Worker(self))

    def start_working(self, timeout=None):
        start = timeit.default_timer()
        for worker in self.workers:
            worker.start()
        try:
            while True:
                end = timeit.default_timer()
                if timeout:
                    if end - start > timeout:
                        raise exception.TimeoutError
                time.sleep(0.01)
        except (KeyboardInterrupt, exception.TimeoutError):
            print('Ending worker threads')
            self.end_threads.set()
            for worker in self.workers:
                worker.join()
            print('All worker threads closed')
            return


class Worker(threading.Thread):
    num_threads = 0

    def __init__(self, manager, name='Worker-'):
        Worker.num_threads += 1
        super(Worker, self).__init__(name=name+str(Worker.num_threads))
        self.daemon = True
        self.manager = manager

    def run(self):
        logging.info('{} started'.format(threading.currentThread().getName()))
        while not self.manager.end_threads.isSet():
            sz = 0
            try:
                page = self.manager.downloader.task_queue.get_nowait()
            except Queue.Empty:
                continue

            print('{} is being downloaded by {}'.format(page, threading.currentThread().getName()))
            logging.info('{} is being downloaded by {}'.format(page, threading.currentThread().getName()))
            try:
                sz = utils.stream_download_image(page.url, page.download_path)
            except exception.MangaDownloadError as e:
                    logging.error(e.message)
                    print('Failed to download page: ' + str(page))
                    self.manager.downloader.add_failed(page)
                    continue
            else:
                with self.manager.lock:
                    self.manager.bytes_downloaded += sz
                    self.manager.downloader.pages_done += 1
                    if self.manager.downloader.pages_done == len(self.manager.downloader.pages):
                        self.manager.end_threads.set()
                print('{}. Completed by {}'.format(page, threading.currentThread().getName()))
                logging.info('{}. Completed by {}'.format(page, threading.currentThread().getName()))

        logging.info('{} closed'.format(threading.currentThread().getName()))
        print('{} closed'.format(threading.currentThread().getName()))
