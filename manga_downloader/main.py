#! /usr/bin/env python

import logging
import os
from worker import WorkerThreadPool
from mangafactory import MangaFactory
import taskmanager
import timeit
import argparse


LOG_PATH = 'log.out'
if os.path.isfile(LOG_PATH):
    os.remove(LOG_PATH)

logging.basicConfig(filename=LOG_PATH, level=logging.INFO, )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('name')
    parser.add_argument('url')
    parser.add_argument('loc')

    args = parser.parse_args()
    name = args.name
    url = args.url
    loc = os.path.join(args.loc, name)
    if not os.path.exists(loc):
        try:
            os.makedirs(loc)
        except os.error:
            logging.error('{} does not exist or write protected!. Quitting..'.format(loc))
            exit(1)

    mangahere = MangaFactory().get_instance('mangahere', url, loc)
    mangahere.fetch_chapters()

    logging.info('{0} chapters found.'.format(len(mangahere.chapters)))
    print('{0} chapters found.'.format(len(mangahere.chapters)))

    # add required chapters in a thread safe queue
    for chapter in mangahere.chapters[0:1]:
        mangahere.add_chapter_to_queue(chapter)

    task_manager = taskmanager.TaskManager(mangahere)
    pool = WorkerThreadPool(mangahere, min(5, max(2, mangahere.chapters_to_download.qsize() // 2)))

    start = timeit.default_timer()

    task_manager.start_all_tasks()
    pool.start_working(timeout=5*60)

    end = timeit.default_timer()
    print('All chapters completed.')
    logging.info('All chapters completed.')

    end_str = '{:.1f} kB downloaded at {:.2f} kBps'.format(pool.bytes_downloaded/1024.0, pool.bytes_downloaded/(1024*(end-start)))
    logging.info(end_str)
    print(end_str)

if __name__ == '__main__':
    main()