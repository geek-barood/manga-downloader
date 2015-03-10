from nose.tools import *
import os
import shutil
from manga_downloader.worker import WorkerThreadPool
from manga_downloader.mangafactory import MangaFactory
from manga_downloader import taskmanager


def test_integrity():
    loc = os.path.join('.', 'test_manga')
    name = 'fairy_tail'
    url = 'http://www.mangahere.co/manga/fairy_tail'
    loc = os.path.join(loc, name)
    if os.path.exists(loc):
        shutil.rmtree(loc)
    else:
        try:
            os.makedirs(loc)
        except os.error:
            exit(1)
    mangahere = MangaFactory().get_instance('mangahere', url, loc)
    mangahere.fetch_chapters()

    assert_greater(len(mangahere.chapters), 0)
    # add required chapters in a thread safe queue
    for chapter in mangahere.chapters[0:1]:
        mangahere.add_chapter_to_queue(chapter)

    task_manager = taskmanager.TaskManager(mangahere)
    pool = WorkerThreadPool(mangahere, min(5, max(2, mangahere.chapters_to_download.qsize() // 2)))

    task_manager.start_all_tasks()
    pool.start_working(timeout=30)
    assert_equal(os.listdir(loc)[0], '0001.vol-01fairy-tail')
    assert_greater(len(os.listdir(os.path.join(loc, '0001.vol-01fairy-tail'))), 0)
    shutil.rmtree(loc)

