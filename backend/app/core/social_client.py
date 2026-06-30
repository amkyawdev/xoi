import httpx
import asyncio
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from app.config import settings


# --- Pydantic Models for Normalized Data ---
class SocialMediaPost(BaseModel):
    platform: str
    id: str
    text: str
    author: str
    likes: int
    shares: int
    comments: int
    url: Optional[str] = None
    created_at: Optional[str] = None


class SocialMediaClient:
    def __init__(self):
        self.rapidapi_key = settings.RAPIDAPI_KEY
        self.youtube_api_key = settings.YOUTUBE_API_KEY
        self.base_headers = {
            "X-RapidAPI-Key": self.rapidapi_key,
            "X-RapidAPI-Host": "social-data-api.p.rapidapi.com"
        }

    async def get_tiktok_video(self, video_id: str) -> Dict[str, Any]:
        """Fetch TikTok video data via RapidAPI"""
        if not self.rapidapi_key:
            return {"error": "RapidAPI key not configured"}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://social-data-api.p.rapidapi.com/tiktok/video",
                headers=self.base_headers,
                params={"video_id": video_id}
            )
            response.raise_for_status()
            return self._normalize_tiktok(response.json())

    async def get_youtube_video(self, video_id: str) -> Dict[str, Any]:
        """Fetch YouTube video data via official API"""
        if not self.youtube_api_key:
            return {"error": "YouTube API key not configured"}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://www.googleapis.com/youtube/v3/videos",
                params={
                    "part": "snippet,statistics",
                    "id": video_id,
                    "key": self.youtube_api_key
                }
            )
            response.raise_for_status()
            return self._normalize_youtube(response.json())

    async def search_social(self, query: str, platforms: List[str] = None) -> List[SocialMediaPost]:
        """Search across multiple platforms"""
        results = []
        if not platforms:
            platforms = ["tiktok", "youtube", "facebook"]
        
        tasks = []
        for platform in platforms:
            if platform == "tiktok":
                tasks.append(self._search_tiktok(query))
            elif platform == "youtube":
                tasks.append(self._search_youtube(query))
            elif platform == "facebook":
                tasks.append(self._search_facebook(query))
        
        all_results = await asyncio.gather(*tasks, return_exceptions=True)
        for res in all_results:
            if isinstance(res, list):
                results.extend(res)
        
        return results

    async def _search_tiktok(self, query: str) -> List[SocialMediaPost]:
        """Search TikTok for content"""
        if not self.rapidapi_key:
            return []
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://social-data-api.p.rapidapi.com/tiktok/search",
                    headers=self.base_headers,
                    params={"query": query}
                )
                response.raise_for_status()
                data = response.json()
                results = []
                for item in data.get("data", [])[:10]:
                    results.append(self._normalize_tiktok(item))
                return results
        except Exception as e:
            return []

    async def _search_youtube(self, query: str) -> List[SocialMediaPost]:
        """Search YouTube for content"""
        if not self.youtube_api_key:
            return []
        
        try:
            async with httpx.AsyncClient() as client:
                # Search for videos
                search_response = await client.get(
                    "https://www.googleapis.com/youtube/v3/search",
                    params={
                        "part": "snippet",
                        "q": query,
                        "type": "video",
                        "maxResults": 10,
                        "key": self.youtube_api_key
                    }
                )
                search_response.raise_for_status()
                search_data = search_response.json()
                
                # Get video IDs
                video_ids = [item["id"]["videoId"] for item in search_data.get("items", [])]
                
                if not video_ids:
                    return []
                
                # Get video details with statistics
                videos_response = await client.get(
                    "https://www.googleapis.com/youtube/v3/videos",
                    params={
                        "part": "snippet,statistics",
                        "id": ",".join(video_ids),
                        "key": self.youtube_api_key
                    }
                )
                videos_response.raise_for_status()
                videos_data = videos_response.json()
                
                results = []
                for item in videos_data.get("items", []):
                    normalized = self._normalize_youtube({"items": [item]})
                    if normalized:
                        results.append(normalized)
                return results
        except Exception as e:
            return []

    async def _search_facebook(self, query: str) -> List[SocialMediaPost]:
        """Search Facebook for content"""
        if not self.rapidapi_key:
            return []
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://social-data-api.p.rapidapi.com/facebook/search",
                    headers=self.base_headers,
                    params={"query": query}
                )
                response.raise_for_status()
                data = response.json()
                results = []
                for item in data.get("data", [])[:10]:
                    results.append(self._normalize_facebook(item))
                return results
        except Exception as e:
            return []

    def _normalize_tiktok(self, raw: Dict) -> SocialMediaPost:
        """Convert TikTok API response to normalized format"""
        return SocialMediaPost(
            platform="tiktok",
            id=raw.get("video_id", raw.get("id", "")),
            text=raw.get("description", raw.get("text", "")),
            author=raw.get("author", {}).get("username", "") if isinstance(raw.get("author"), dict) else raw.get("author", ""),
            likes=raw.get("stats", {}).get("like_count", 0),
            shares=raw.get("stats", {}).get("share_count", 0),
            comments=raw.get("stats", {}).get("comment_count", 0),
            url=raw.get("video_url", ""),
            created_at=raw.get("created_at", raw.get("create_time", ""))
        )

    def _normalize_youtube(self, raw: Dict) -> Optional[SocialMediaPost]:
        """Convert YouTube API response to normalized format"""
        items = raw.get("items", [])
        if not items:
            return None
        item = items[0]
        snippet = item.get("snippet", {})
        stats = item.get("statistics", {})
        return SocialMediaPost(
            platform="youtube",
            id=item.get("id", ""),
            text=snippet.get("description", ""),
            author=snippet.get("channelTitle", ""),
            likes=int(stats.get("likeCount", 0)) if stats.get("likeCount") else 0,
            shares=0,  # YouTube doesn't provide share count in v3
            comments=int(stats.get("commentCount", 0)) if stats.get("commentCount") else 0,
            url=f"https://www.youtube.com/watch?v={item.get('id')}",
            created_at=snippet.get("publishedAt")
        )

    def _normalize_facebook(self, raw: Dict) -> SocialMediaPost:
        """Convert Facebook API response to normalized format"""
        return SocialMediaPost(
            platform="facebook",
            id=raw.get("id", raw.get("post_id", "")),
            text=raw.get("message", raw.get("text", "")),
            author=raw.get("from", {}).get("name", "") if isinstance(raw.get("from"), dict) else raw.get("from", ""),
            likes=raw.get("likes", {}).get("summary", {}).get("total_count", 0) if isinstance(raw.get("likes"), dict) else 0,
            shares=raw.get("shares", {}).get("count", 0) if isinstance(raw.get("shares"), dict) else raw.get("shares", 0),
            comments=raw.get("comments", {}).get("summary", {}).get("total_count", 0) if isinstance(raw.get("comments"), dict) else 0,
            url=raw.get("permalink_url", ""),
            created_at=raw.get("created_time", "")
        )


# Singleton instance
social_client = SocialMediaClient()
