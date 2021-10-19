BOT_NAME = 'estimation_tool'
SPIDER_MODULES = ['estimation_tool_scrapy.spiders']
NEWSPIDER_MODULE = 'estimation_tool_scrapy.spiders'
LOG_LEVEL = 'WARNING'
LOG_FILE = 'error.log'
ROBOTSTXT_OBEY = False

HTTP_PROXY = 'http://127.0.0.1:8118'
USER_AGENT = 'APIs-Google (+https://developers.google.com/webmasters/APIs-Google.html)'
# DEFAULT_REQUEST_HEADERS = {}


# CONCURRENT_REQUESTS = 16
# DOWNLOAD_DELAY = 2
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16


PROXY_POOL_ENABLED = False
PROXY_POOL_TRY_WITH_HOST = False
# PROXY_POOL_PAGE_RETRY_TIMES = 10
# PROXY_POOL_FORCE_REFRESH = True
# PROXY_POOL_FILTER_CODE = 'jp'

DOWNLOADER_MIDDLEWARES = {
	# 'estimation_tool_scrapy.middlewares.ProxyMiddleware': 543,
	'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
	'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
	# 'scrapy_proxy_pool.middlewares.ProxyPoolMiddleware': 610,
	# 'scrapy_proxy_pool.middlewares.BanDetectionMiddleware': 620,
}

ITEM_PIPELINES = {
	'estimation_tool_scrapy.pipelines.EstimationToolPipeline': 300,
}
