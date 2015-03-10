class Page:
    def __init__(self, chapter, url, download_path):
        self.chapter = chapter
        self.url = url
        self.download_path = download_path

    @property
    def __repr__(self):
        return 'Page(chapter:{0}, url:{1}, download_path:{2})'.\
            format(self.chapter, self.url, self.download_path)

    def __str__(self):
        return 'Page(chapter:{0}, url:{1}, download_path:{2})'.\
            format(self.chapter, self.url, self.download_path)


class Chapter:
    def __init__(self, name, number, url):
        self.name = name
        self.number = number
        self.url = url

    @property
    def __repr__(self):
        return 'Chapter(name:{0}, number:{1}, url:{2})'.\
            format(self.name, self.number, self.url)

    def __str__(self):
        return 'Chapter(name:{0}, number:{1}, url:{2})'.\
            format(self.name, self.number, self.url)