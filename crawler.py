import scrapy

from settings import APP_URI, APP_USERNAME, APP_PASSWORD
from urlparse import urljoin

class AppCrawler(scrapy.Spider):
    '''
    basic spider crawler
    '''
    name = 'app_crawler'
    start_urls = [urljoin(APP_URI,'login.php')]

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={
                'username': APP_USERNAME,
                'password': APP_PASSWORD,
            },
            callback=self.after_login)

    def after_login(self, response):
        '''
        Look for vulnerable input fields
        '''
        # handle login as suggested by docs
        # https://doc.scrapy.org/en/latest/topics/request-response.html#using-formrequest-to-send-data-via-http-post
        if "authentication failed" in response.body:
            self.logger.error("Login failed")
            return
        else:
            # This could be an extra argument to the crawler
            selector = 'input'
            self.logger.info(response.xpath(selector))
            return response.xpath(selector)
            
    
