import model
import logging
import requests
import exception
import os
import bs4

from bs4 import BeautifulSoup, SoupStrainer
from mangadownloader import MangaDownloader


class MangaHere(MangaDownloader):
    def __init__(self):
        super(MangaHere, self).__init__()

    def add_chapter_pages_task(self, chapter, download_dir):
        curr_url = chapter.url
        while not self.got_stop_request():
            try:
                curr_page_resp = requests.get(curr_url)
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                raise exception.RequestError('Request error for: {0}'.format(str(chapter)))

            if curr_page_resp.status_code == 200:
                curr_page = curr_page_resp.text
            else:
                raise exception.RequestError(
                    '[{0}] Error response code {1}'.format(curr_page_resp.status_code, curr_url))

            viewer = SoupStrainer(id='viewer')
            curr_soup = BeautifulSoup(curr_page, parse_only=viewer)
            if curr_soup is None:

                raise exception.PageDownloadError('Failed to parse image url from the page')
            try:
                link = curr_soup.find(id='image')['src']
                image_url = link[:link.find('?')].strip()
                next_page_url = curr_soup.a['href'].strip()

                file_name = image_url[image_url.rfind('/') + 1:]
                download_path = os.path.join(download_dir, file_name)
                page = model.Page(chapter, image_url, download_path)
            except TypeError:
                print('Failed to parse image url from the page')
                logging.error('Failed to parse image url from the page')
            else:
                self.add_page_to_queue(page)
                logging.info('Added {0} to queue'.format(page))
                print('Added {0} to queue'.format(page))
                if next_page_url[:4] != 'http':
                    break
                curr_url = next_page_url

    @staticmethod
    def get_chapters_from_soup(soup):
        """
        returns:
            list(model.Chapter(name, number, url))
        """
        spans = soup.find_all('span', class_=u'left')
        chapters = []
        for span in spans:
            if type(span.a) is bs4.element.Tag:
                chapters.append(
                    model.Chapter(span.get_text()[span.get_text().rfind('\n'):].strip(),
                                  span.a.text.strip().split()[-1],
                                  span.a['href'])
                )

        return chapters

    def fetch_chapters(self):
        try:
            page_resp = requests.get(self.url)
            # hack to check whether the url is from mangahere or not
            if str(page_resp.headers['set-cookie']).rfind('mangahere.co') != -1:
                if page_resp.status_code == 200:
                    page = page_resp.text
                else:
                    raise exception.RequestError

        except (requests.exceptions.Timeout,
                requests.exceptions.ConnectionError):
            logging.error('Error getting base url:', self.url)
            raise exception.RequestError
        else:
            divs = SoupStrainer('div')
            soup = BeautifulSoup(page, parse_only=divs)
            logging.info('Crawling for chapters.')

            self.chapters = self.get_chapters_from_soup(soup)
            self.chapters.reverse()



