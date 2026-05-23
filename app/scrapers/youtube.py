from datetime import datetime, timedelta, timezone
from typing import Optional
import feedparser
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from pydantic import BaseModel


class Transcript(BaseModel):
    text: str

class ChannelVideo(BaseModel):
    title: str
    url: str
    channel_id: str
    video_id: str
    published_at: datetime
    description: str
    transcript: Optional[str] = None


class YouTubeScraper:
    def __init__(self):
        self.transcript_api = YouTubeTranscriptApi()

    def get_rss_url(self, channel_id: str) -> str:
        """Create URL for a channel."""
        return f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"

    def extract_video_id(self, video_url: str) -> str:
        """Extract video id from a YouTube URL."""
        if "youtube.com/watch?v=" in video_url:
            return video_url.split("v=")[1].split("&")[0]
        if "youtu.be/" in video_url:
            return video_url.split("youtu.be/")[1].split("?")[0]
        return video_url

    def get_videos(self, channel_id: Optional[str] = None, hours: Optional[int] = 168) -> list[ChannelVideo]:
        feed = feedparser.parse(self.get_rss_url(channel_id))

        if not feed.entries:
            print(f"❌ Không có videos nào từ channel {channel_id}")
            return []

        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)

        videos = []
        for entry in feed.entries:
            published_time = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
            if published_time >= cutoff_time:
                video_id = self.extract_video_id(entry.link)
                videos.append(ChannelVideo(
                    title=entry.title,
                    url=entry.link,
                    channel_id=channel_id,
                    video_id=video_id,
                    published_at=published_time,
                    description=entry.get("summary", "")
                ))

        return videos

    def get_transcripts(self, video_id: str) -> Optional[Transcript]:
        try:
            transcript_list = self.transcript_api.fetch(video_id)
            return Transcript(text=" ".join([snipet.text for snipet in transcript_list]))
        except (TranscriptsDisabled, NoTranscriptFound):
            return None
        except Exception:
            return None

    def scrape_channel(self, channel_id: str, hours: int = 168) -> list[ChannelVideo]:
        videos = self.get_latest_videos(channel_id, hours)
        result = []
        for video in videos:
            transcript = self.get_transcripts(video.video_id)
            result.append(video.model_copy(update={"transcript": transcript.text if transcript else None}))
        return result
    
if __name__ == "__main__":
    scraper = YouTubeScraper()
    videos = scraper.get_videos("UCawZsQWqfGSbCI5yjkdVkTA")

    print(f"Da tim duoc {len(videos)} videos")
    print(videos[0])

