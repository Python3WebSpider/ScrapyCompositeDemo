# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import aiohttp
import logging


class AuthorizationMiddleware(object):
    accountpool_url = 'http://192.168.2.3:6777/antispider7/random'
    logger = logging.getLogger('middlewares.authorization')

    async def process_request(self, request, spider):
        async with aiohttp.ClientSession() as client:
            response = await client.get(self.accountpool_url)
            if not response.status == 200:
                return
            credential = await response.text()
            authorization = f'jwt {credential}'
            self.logger.debug(f'set authorization {authorization}')
            request.headers['authorization'] = authorization


class ProxyMiddleware(object):
    proxypool_url = 'http://192.168.2.3:5555/random'
    logger = logging.getLogger('middlewares.proxy')

    async def process_request(self, request, spider):
        async with aiohttp.ClientSession() as client:
            response = await client.get(self.proxypool_url)
            if not response.status == 200:
                return
            proxy = await response.text()
            self.logger.debug(f'set proxy {proxy}')
            request.meta['proxy'] = f'http://{proxy}'
