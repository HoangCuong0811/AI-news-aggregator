from datetime import datetime, timedelta, timezone
from typing import Optional
import feedparser
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound


def get_rss_url(channel_id: str) -> str:
    """
    Create URL for a channel
    """
    return f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"


def extract_video_id(video_url: str) -> str:
    """
        Extract video id from an URL
    """
    if "youtube.com/watch?v=" in video_url:
        return video_url.split("v=")[1].split("&")[0]
    if "youtu.be/" in video_url:
        return video_url.split("youtu.be/")[1].split("?")[0]
    return video_url


def get_latest_videos(channel_id: str, hours: int = 100) -> list[dict]:
    feed = feedparser.parse(get_rss_url(channel_id))
    ### get youtube channel info and videos from URL

    if not feed.entries:
        print(f"❌ Không có videos nào từ channel {channel_id}")
        return []

    print(f"✅ Tìm thấy {len(feed.entries)} videos trong feed")

    cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)
    print(f"⏰ Tìm videos từ {cutoff_time}")
    ###  giả sử hours = 24 (1 ngày), tính thời gian 1 ngày trước

    videos = []

    for entry in feed.entries:
        published_time = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
        if published_time >= cutoff_time:
            video_id = extract_video_id(entry.link)
            videos.append({
                "title": entry.title,
                "url": entry.link,
                "video_id": video_id,
                "published_at": published_time.isoformat(),
                "description": entry.get("summary", ""),
            })
        else:
            print(f"⏭️  Bỏ qua video cũ: {entry.title} (published: {published_time})")

    print(f"📹 Tìm thấy {len(videos)} videos mới")
    return videos

def get_transcripts(video_id: str) -> Optional[str]:
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([entry["text"] for entry in transcript_list])
    except(TranscriptsDisabled, NoTranscriptFound):
        return None
    except:
        return None
    
    
if __name__ == "__main__":
    videos = get_latest_videos("UCn8ujwUInbJkBhffxqAPBVQ")
    print(videos)