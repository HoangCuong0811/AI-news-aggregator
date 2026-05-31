from typing import Optional
from scrapers.youtube import YouTubeScraper
from database.repository import Repository

def process_videos_transcript(limit: Optional[int] = None) -> dict:
    scraper = YouTubeScraper()
    repo = Repository()

    videos = repo.get_videos_without_transcript()
    if videos:
        for v in videos:
            transript = scraper.get_transcripts(v.video_id)
            repo.update_youtube_transcript(v.video_id, transcript=transript.text)
    return "Update all youtube videos transcript sucessfullly"

if __name__ == "__main__":
    print(process_videos_transcript())

