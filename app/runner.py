from app.config import YOUTUBE_CHANNEL
from app.database.connection import get_session
from app.database.repository import Repository
from app.scrapers.anthropic import AnthropicScraper
from app.scrapers.openai import OpenAIScraper
from app.scrapers.youtube import YouTubeScraper


def run_scrapers(hours: int = 200) -> dict:
    youtube_scraper = YouTubeScraper()
    openai_scraper = OpenAIScraper()
    anthropic_scraper = AnthropicScraper()
    repo = Repository()

    youtube_videos = []
    for channel_id in YOUTUBE_CHANNEL:
        videos = youtube_scraper.get_videos(channel_id, hours)
        youtube_videos.extend(videos)

    openai_articles = openai_scraper.get_articles(hours)
    anthropic_articles = anthropic_scraper.get_articles(hours)

    if youtube_videos:
        repo.create_youtube_videos(youtube_videos)

    if openai_articles:
        repo.create_openai_articles(openai_articles)

    if anthropic_articles:
        repo.create_anthropic_articles(anthropic_articles)

    return {
        "youtube": youtube_videos,
        "anthropic": anthropic_articles,
        "openai": openai_articles,
    }




