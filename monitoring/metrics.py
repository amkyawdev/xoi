"""Prometheus metrics"""

from prometheus_client import Counter, Histogram, Gauge, generate_latest


# Counters
request_count = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

# Histograms
request_duration = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration",
    ["method", "endpoint"]
)

# Gauges
active_connections = Gauge(
    "active_connections",
    "Number of active connections"
)

llm_calls = Counter(
    "llm_calls_total",
    "Total LLM API calls",
    ["model", "status"]
)

crawl_pages = Counter(
    "crawled_pages_total",
    "Total pages crawled"
)


def get_metrics() -> bytes:
    """Get metrics in Prometheus format"""
    return generate_latest()
