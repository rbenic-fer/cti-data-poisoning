import scrapy

from bs4 import BeautifulSoup

SAVE_DIR = 'articles'
FILE_NAME = SAVE_DIR + '/content.txt'
HEADERS = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.7113.93 Safari/537.36',
    'Referer':'None'
}

class ArticlesSpider(scrapy.Spider):
    name = 'articles'
    start_urls = [
        'https://krebsonsecurity.com/page/1/'
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers=HEADERS)

    def parse(self, response):
        page = response.url.split("/")[-2]
        save_file = SAVE_DIR + '/krebs-on-security-' + page + '.html'
        with open(save_file, 'wb') as f:
            f.write(response.body)

        with open(FILE_NAME, 'a') as f:
            for entry in response.css('div.entry-content'):
                for paragraph in entry.css('div.entry-content > p').getall():
                    soup = BeautifulSoup(paragraph, features='lxml')

                    more_link = soup.find('a', 'more-link')
                    if more_link != None:
                        more_link.extract()

                    text = soup.get_text()
                    if text == None:
                        continue
                    text = text.strip()
                    if len(text) == 0:
                        continue

                    print(text, end='\n\n', file=f)

                print(file=f)

        yield from response.follow_all(css='li a.inactive::attr(href)', headers=HEADERS, callback=self.parse)
