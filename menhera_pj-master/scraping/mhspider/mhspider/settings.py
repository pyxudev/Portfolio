BOT_NAME = 'mhspider'
SPIDER_MODULES = ['mhspider.spiders']
NEWSPIDER_MODULE = 'mhspider.spiders'

LOG_LEVEL = 'WARNING'
LOG_FILE = 'error.log'

HTTP_PROXY = 'http://127.0.0.1:8118'

USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0'

ROBOTSTXT_OBEY = False
# DEFAULT_REQUEST_HEADERS = {}


#CONCURRENT_REQUESTS = 1
DOWNLOAD_DELAY = 0.5
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16


PROXY_POOL_ENABLED = False
PROXY_POOL_TRY_WITH_HOST = False
# PROXY_POOL_PAGE_RETRY_TIMES = 10
# PROXY_POOL_FORCE_REFRESH = True
# PROXY_POOL_FILTER_CODE = 'jp'

DOWNLOADER_MIDDLEWARES = {
	'mhspider.middlewares.ProxyMiddleware': 543,
	'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
	'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
#	'scrapy_proxy_pool.middlewares.ProxyPoolMiddleware': 610,
#	'scrapy_proxy_pool.middlewares.BanDetectionMiddleware': 620,
}

ITEM_PIPELINES = {
	'mhspider.pipelines.MhspiderPipeline': 300,
}
