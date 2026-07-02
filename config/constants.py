"""Application constants"""

# API
DEFAULT_PORT = 8000
DEFAULT_HOST = "0.0.0.0"
MAX_REQUEST_SIZE = 10 * 1024 * 1024  # 10MB

# Crawler
DEFAULT_CRAWL_DEPTH = 2
MAX_CRAWL_DEPTH = 10
CRAWL_TIMEOUT = 30
MAX_CONCURRENT_CRAWLS = 10

# LLM
DEFAULT_MODEL = "gpt-4"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 4096

# Cache
DEFAULT_CACHE_TTL = 300  # 5 minutes
MAX_CACHE_TTL = 3600  # 1 hour

# Rate Limiting
DEFAULT_RATE_LIMIT = 60  # requests per minute
RATE_LIMIT_WINDOW = 60  # seconds

# Pagination
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# Search
DEFAULT_SEARCH_LIMIT = 10
MAX_SEARCH_LIMIT = 50

# Vector Store
DEFAULT_EMBEDDING_MODEL = "text-embedding-ada-002"
EMBEDDING_DIMENSIONS = 1536

# Storage
STORAGE_DIRS = {
    "html": "storage/html",
    "markdown": "storage/markdown",
    "cache": "storage/cache",
    "vectors": "storage/vectors",
    "outputs": "storage/outputs"
}
