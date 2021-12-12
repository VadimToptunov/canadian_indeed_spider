import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class IndeedCompaniesSpider(CrawlSpider):
    name = 'indeed_companies'
    allowed_domains = ['ca.indeed.com']
    start_urls = ['https://ca.indeed.com/companies/']
    # rules = Rule(LinkExtractor(callback='parse', follow=True),)
    rules = (
        Rule(LinkExtractor(allow="/cmp/*/", deny="/cmp/*/*"), callback="parse", follow=True),)

    def parse(self, response):
        self.log('crawling'.format(response.url))
        yield
