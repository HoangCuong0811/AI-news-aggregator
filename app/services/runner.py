from typing import List
from services.config import YOUTUBE_CHANNEL
from scrapers.anthropic import AnthropicScraper
from scrapers.openai import OpenAIScraper
from scrapers.youtube import YouTubeScraper

def run_scrapers(hours: int = 168):
    youtube_scraper = YouTubeScraper()
    anthropic_scraper = AnthropicScraper()
    openai_scraper = OpenAIScraper()

    videos = []
    for channel_id in YOUTUBE_CHANNEL:
        video = youtube_scraper.get_videos(channel_id, hours)
        videos.extend(video)

    anthropics = anthropic_scraper.get_articles(hours)
    openais = openai_scraper.get_articles(hours)


    return {
        "videos": videos,
        "anthropics": anthropics,
        "openais": openais
    }

if __name__ == "__main__":
    import json
    
    print("Bắt đầu chạy scraper...")
    result = run_scrapers(168)
    
    print(f"✅ Đã tìm thấy:")
    print(f"- {len(result['videos'])} videos")
    print(f"- {len(result['anthropics'])} bài viết Anthropic")
    print(f"- {len(result['openais'])} bài viết OpenAI\n")
    
    # In dạng JSON làm đẹp (pretty print)
    # Lấy các kết quả ra, gọi schema_model.model_dump() để chuyển Object về Dictionary
    # Sử dụng indent=4 để thụt lề, default=str để tự động ép kiểu datetime sang chuỗi
    print(json.dumps({
        "videos": [video.model_dump() for video in result["videos"]],
        "anthropics": [article.model_dump() for article in result["anthropics"]],
        "openais": [article.model_dump() for article in result["openais"]]
    }, indent=4, ensure_ascii=False, default=str))
    
    print(result["videos"])
    
