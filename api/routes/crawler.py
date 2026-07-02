"""Crawler routes"""

from fastapi import APIRouter, Depends

from api.dependencies import FetcherDep
from api.schemas import CrawlRequest, CrawlResponse


router = APIRouter()


@router.post("/scrape", response_model=dict)
async def scrape_url(request: CrawlRequest, fetcher: FetcherDep) -> dict:
    """Scrape a single URL"""
    result = await fetcher.fetch(request.url)
    return result


@router.post("/crawl", response_model=CrawlResponse)
async def crawl(request: CrawlRequest, fetcher: FetcherDep) -> CrawlResponse:
    """Crawl starting from URL"""
    result = await fetcher.fetch(request.url)
    
    return CrawlResponse(
        url=result.get("url", request.url),
        status=result.get("status", 0),
        content=result.get("content", ""),
        links=[]
    )
