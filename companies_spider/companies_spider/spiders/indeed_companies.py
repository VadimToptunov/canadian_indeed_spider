from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class IndeedCompaniesSpider(CrawlSpider):
    name = 'indeed_companies'
    allowed_domains = ['ca.indeed.com']
    start_urls = ['https://ca.indeed.com/companies/']
    rules = (
        Rule(LinkExtractor(allow=r"/cmp/*/",
                           deny=(r'jobs', r'reviews', r'faq', r'salaries', r'/survey/mc*',
                                 r'interviews', r'photos', r'questions', r'write-review', r"topics",
                                 r"articles", r"benefits", r"locations")),
             callback="parse", follow=True),)

    def parse(self, response):
        href = response.css("a.css-iigu5k.emf9s7v0[aria-label='Why Join Us']::attr(href)").get()
        yield response.follow(href, callback=self.parse_with_social_data)

    def parse_with_social_data(self, response):
        page = response.url.replace("/about", "")
        stars = response.css("span.css-htn3vt.e1wnkr790::text").get()
        if stars is not None:
            stars = float(stars)
        title = response.css("[itemprop='name']::text").get()
        industry = response.css("[data-tn-element='industryLink']::text").get()
        jobs_number = response.css("[data-tn-element='jobs-tab'] .css-r228jg::text").get()
        headquarters = response.css("[data-testid='headquarters']::text").get()
        if headquarters is not None:
            headquarters = ' '.join(headquarters.splitlines())
        links = response.css("[data-tn-element='companyLink[]']::attr(href)").extract()
        twitter = response.css("a.twitter-timeline::attr(href)").extract()
        facebook = response.css("div.fb-page::attr(data-href)").extract()

        company_data_with_social_media = {
            "url": page,
            "stars": stars,
            "title": title,
            "industry": industry,
            "jobs_number": jobs_number,
            "headquarters": headquarters,
            "links": links,
            "twitter": twitter,
            "facebook": facebook
        }
        print(company_data_with_social_media)
        yield company_data_with_social_media
