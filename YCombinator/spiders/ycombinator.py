import scrapy


class YcombinatorSpider(scrapy.Spider):
    name = 'ycombinator'
    start_urls = [f'https://www.workatastartup.com/jobs?page={page}' for page in range(1, 10)]

    def parse(self, response):
        for job in response.css('div.jobs-list div'):
            yield {
                'company_name': job.css('div.company-details a span.font-bold::text').get("").strip(),
                'company_url': job.css('div.company-details a::attr(href)').get(),
                'job_name': job.css('div.job-name a::text').get("").strip(),
                'job_url': job.css('div.job-name a::attr(href)').get(),
            }
