"""Search routes"""

from fastapi import APIRouter

from api.schemas import SearchRequest, SearchResponse


router = APIRouter()


@router.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest) -> SearchResponse:
    """Search the web"""
    # Placeholder - would integrate with search API
    return SearchResponse(
        results=[
            {
                "title": "Example Result",
                "url": "https://example.com",
                "snippet": "This is a placeholder search result."
            }
        ],
        total=1
    )
