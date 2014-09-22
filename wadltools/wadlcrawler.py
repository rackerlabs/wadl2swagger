import mechanize
import os, errno

class WADLCrawler:
    def __init__(self):
        self.browser = mechanize.Browser()

    def crawl(self, url):
        br = self.browser
        br.open(url)
        response = br.response()
        wadl_files = []
        for link in br.links():
            if link.url.endswith('.wadl'):
                wadl_files.append(link.absolute_url)
        return wadl_files

    def download(self, url, target_file):
        br = self.browser
        br.open(url)
        f = open(target_file, 'w')
        f.write(br.response().read())
        f.close
