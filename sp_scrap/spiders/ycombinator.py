from textwrap import indent
import scrapy
import json
from bson.objectid import ObjectId


class YcombinatorSpider(scrapy.Spider):
    name = 'ycombinator'
    start_urls = [f'https://www.workatastartup.com/jobs?page={page}' for page in range(1, 10)]

    def parse(self, response):
        for job in response.css('div.jobs-list div'):
            job_page = job.css('div.job-name a::attr(href)').get()
            
            if job_page is not None:
                yield response.follow(job_page, self.parse_job)

    def parse_job(self, response):
        company_page = response.css('div.company-logo span a::attr(href)').get('').strip()
        yield response.follow(company_page, self.parse_company)

    def parse_company(self, response):
        json_data = json.loads(response.css('.js-react-on-rails-component::text').get()).get('rawCompany')
        
        if json_data is not None:
            founders = [
                {
                    '_id': founder['linkedin'],
                    'collection': 'founders',
                } 
                for founder 
                in json_data['founders']
            ]

            jobs = [
                {
                    '_id': job['show_path'],
                    'collection': 'jobs',
                    **job,
                } 
                for job
                in json_data['jobs']
            ]

            del json_data['jobs']
            del json_data['founders']
            
            json_data['founders'] = founders
            
            json_data['jobs'] = [
                {
                    '_id': job['_id'],
                    'collection': 'jobs',
                }
                for job
                in jobs
            ]

            yield {
                'collection': 'companies',
                '_id': response.url,
                **json_data,
            }

            for founder in founders:
                yield founder

            for job in jobs:
                yield job
