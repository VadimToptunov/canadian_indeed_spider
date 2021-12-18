import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class IndeedCompaniesSpider(CrawlSpider):
    name = 'indeed_companies'
    allowed_domains = ['ca.indeed.com']
    start_urls = ['https://ca.indeed.com/companies/']
    rules = (
        Rule(LinkExtractor(allow=r"/cmp/*/", deny=(r'jobs', r'reviews', r'faq', r'salaries', r'survey', r'about',
                                                   r'interviews', r'photos', r'questions')),
             callback="parse", follow=True),)

    def parse(self, response):
        page = response.url
        stars = response.css(".css-htn3vt e1wnkr790::text").get()
        title = response.css("head title::text").get().replace("\n", " ")\
            .replace("Careers and Employment | Indeed.com", "")
        industry = response.css("[data-testid='companyInfo-industry'] .css-1w0iwyp::text").get()
        jobs_num = response.css("[data-tn-element='jobs-tab'] .css-r228jg::text").get()
        self.log('crawling'.format(page))
        print(f"{page}, {title}, {industry}, {jobs_num}")
        yield {
            "url": page,
            "stars": stars,
            "title": title,
            "industry": industry,
            "jobs_number": jobs_num
        }
